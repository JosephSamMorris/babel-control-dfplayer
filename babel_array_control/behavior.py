import time
import numpy as np
import random
import math
import json
import perlin
from threading import Thread
from lights import unit_index_from_pos

noise = perlin.Perlin(824393)

UNIT_COUNT = 180
ARRAY_COLUMNS = 13
ARRAY_ROWS = 14

DEBUG_SEE_PEOPLE = False


def constrain(v, vmin, vmax):
    if v < vmin:
        return vmin
    elif v > vmax:
        return vmax

    return v


class SimPerson:
    def __init__(self):
        self.max_lifetime = 120
        self.time = 0

        # Most people walk through the center so let's sample from a centered normal distribution
        self.x = np.random.normal(scale=13 / 4) + 13 / 2
        self.x = 0 if self.x < 0 else self.x
        self.x = ARRAY_COLUMNS - 1 if self.x >= ARRAY_COLUMNS else self.x

        # Randomly start at the top or bottom, walking down or up, respectively
        self.y = random.choice([0, ARRAY_ROWS - 1])
        self.direction = math.pi / 2 if self.y == 0 else -math.pi / 2

        # Tweak path
        self.direction += math.pi / 4 * (2 * random.random() - 1)

        self.speed = 1.0
        self.random_speed()

        self.waiting = False
        self.time_waiting = None
        self.time_to_wait = None

        self.alive = True

    def die(self):
        self.alive = False

    def random_speed(self):
        min_speed = 0.05
        max_speed = 0.5
        self.speed = random.random() * (max_speed - min_speed) + min_speed

    def update(self, dt):
        chance_of_stopping = 0.1
        min_time_wait = 10
        max_time_wait = 30  # They are only loaded with this much audio anyway

        if self.waiting:
            self.time_waiting += dt

            if self.time_waiting > self.time_to_wait:
                # Stop waiting
                self.waiting = False

                # Start moving again
                self.random_speed()
        else:
            # Sometimes stop and look/listen
            if random.random() < chance_of_stopping * dt:
                self.speed = 0
                self.time_waiting = 0

                # Decide how long to stop for
                self.time_to_wait = random.random() * (max_time_wait - min_time_wait) + min_time_wait

                self.waiting = True

        self.x += self.speed * math.cos(self.direction) * dt
        self.y += self.speed * math.sin(self.direction) * dt

        # Enforce collision with the walls
        if self.x < 0:
            self.x = 0
            self.direction = math.atan2(math.sin(self.direction), -math.cos(self.direction))
        elif self.x >= ARRAY_COLUMNS:
            self.x = ARRAY_COLUMNS-1
            self.direction = math.atan2(math.sin(self.direction), -math.cos(self.direction))
        if self.y < 0 or self.y > ARRAY_ROWS:
            # Left the space
            self.die()

        self.time += dt

        # Kill if too old (stuck?)
        if self.time > self.max_lifetime:
            self.die()


class BabelBehavior:
    def __init__(self, array_server, rate=5):
        self.array_server = array_server
        self.update_thread = Thread(target=self.update_thread_fn, daemon=True)
        self.rate = rate
        self.time = 0

        self.brightness = [0] * UNIT_COUNT
        self.volume = [0] * UNIT_COUNT

        # Where each unit tries to return to
        self.clear_mask = [1] * UNIT_COUNT

        punch_outs = [
            (8, 11, 2),
        ]

        for x, y, r in punch_outs:
            d = 2 * r

            for off_y in range(d):
                for off_x in range(d):
                    c_off_x = off_x - r
                    c_off_y = off_y - r
                    dist = math.sqrt(c_off_x ** 2 + c_off_y ** 2)

                    if dist > r:
                        # Only touch units within the quiet radius
                        continue

                    off_idx = unit_index_from_pos(x + c_off_x, y + c_off_y)

                    if off_idx is None:
                        continue

                    dist_factor = dist / r
                    self.clear_mask[off_idx] = dist_factor

        self.people = [SimPerson()]

    def render(self):
        if DEBUG_SEE_PEOPLE:
            for i in range(UNIT_COUNT):
                self.brightness[i] = 0
                self.volume[i] = 0

            for person in self.people:
                x = int(person.x)
                y = int(person.y)
                idx = unit_index_from_pos(x, y)
                self.brightness[idx] = 1
                self.volume[idx] = 1

            return

        # Update the clear mask

        min_volume = 0.2
        max_volume = 0.8

        for y in range(ARRAY_ROWS):
            for x in range(ARRAY_COLUMNS):
                idx = unit_index_from_pos(x, y)

                if idx is None:
                    continue

                prl = noise.three(x * 500, y * 500, self.time * 50 + 10)
                b = (1 - constrain(-prl, 0, 20) / 20) * (max_volume - min_volume) + min_volume
                self.clear_mask[idx] = b

        transition_time = 3
        silent_radius = 2  # How many units to make silent around someone who has stopped
        quiet_radius = 4  # How many units to make quiet around someone who has stopped

        # Clear (gently)
        for i in range(UNIT_COUNT):
            self.brightness[i] += (self.clear_mask[i] - self.brightness[i]) / 2.0
            self.volume[i] += (self.clear_mask[i] - self.volume[i]) / 2.0

        for person in self.people:
            x = int(person.x)
            y = int(person.y)

            idx = unit_index_from_pos(x, y)

            if idx is None:
                # Skip if out of bounds
                continue

            if person.waiting:
                # Lerp this from zero to some value to animate volume transition
                # From zero to 1
                intensity = 1 - constrain(transition_time - person.time_waiting, 0, transition_time) / transition_time
                d = quiet_radius * 2

                for off_y in range(d):
                    for off_x in range(d):
                        # Bring the brightness / volume down
                        c_off_x = off_x - quiet_radius
                        c_off_y = off_y - quiet_radius
                        dist = math.sqrt(c_off_x ** 2 + c_off_y ** 2)

                        if dist > quiet_radius:
                            # Only touch units within the quiet radius
                            continue

                        off_idx = unit_index_from_pos(x + c_off_x, y + c_off_y)

                        if off_idx is None:
                            continue

                        if dist < silent_radius:
                            b = 1 - intensity
                        else:
                            # 0 to 1 from edge of inner silent to border
                            dist_factor = (dist - silent_radius) / (quiet_radius - silent_radius)
                            b = max(1 - intensity, dist_factor)

                        # Don't mess with quietings in progress
                        self.brightness[off_idx] = min(self.brightness[off_idx], b)
                        self.volume[off_idx] = min(self.volume[off_idx], b)

                # Make the one above them loud
                self.brightness[idx] = intensity
                self.volume[idx] = intensity

    def update_sim(self, dt):
        chance_of_person = 0.1 * dt

        # Sometimes create people
        if random.random() < chance_of_person:
            self.people.append(SimPerson())

        for person in self.people:
            person.update(dt)

        # Remove the dead people
        self.people = [p for p in self.people if p.alive]

    def update_thread_fn(self):
        while True:
            dt = 1.0 / self.rate

            self.update_sim(dt)
            self.render()

            cmd = json.dumps({
                'command': 'blit',
                'brightness': self.brightness,
                'volume': self.volume,
            })
            self.array_server.handle_behavior_request(cmd)

            time.sleep(dt)
            self.time += dt

    def start(self):
        self.update_thread.start()
