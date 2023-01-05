import math
import random
from ..lights import unit_pos_from_index, unit_index_from_pos, in_bounds, UNIT_COUNT, ARRAY_ROWS, ARRAY_COLUMNS
from ..units_info import get_units_by_priority
from .behavior import Behavior
from .util import distance, find_distant_unit


class RainDrop:
    def __init__(self, x, y, thickness, speed=1, lifetime=30):
        self.x = x
        self.y = y

        # Thickness of the wave emitted by the droplet in # of units
        self.thickness = thickness
        self.speed = speed
        self.lifetime = lifetime

        self.alive = True
        self.time = 0

    def radius(self):
        return self.time * self.speed

    def update(self, dt):
        self.time += dt

        if self.time > self.lifetime:
            self.alive = False


class RainDropsBehavior(Behavior):
    def __init__(self):
        super().__init__({
            'chance_of_raindrop': 0.3,
            'breathing_period': 2,
            'max_units_active': 20,
            'units_to_highlight': list(map(lambda info: info['index'], filter(lambda info: not info['musical'], get_units_by_priority(2)))),
            'min_distance': 2,
            'min_brightness': 0.2,
            'droplet_lifetime': 90,
            'droplet_wave_thickness': 3,
            'droplet_wave_speed': 2,
        })

        self.droplets = []
        self.new_droplet()

    def new_droplet(self):
        # Randomly pick a unit from those that should be highlighted
        # and create a new droplet on top of it
        avoid_indices = list(map(lambda u: unit_index_from_pos(u.x, u.y), self.droplets))
        unit_index = find_distant_unit(self.params['units_to_highlight'], avoid_indices, self.params['min_distance'])

        if unit_index is None:
            # We failed to find a unit that satisfies the min distance constrain so we'll not add a droplet
            return

        x, y = unit_pos_from_index(unit_index)
        self.droplets.append(RainDrop(
            x, y,
            self.params['droplet_wave_thickness'],
            self.params['droplet_wave_speed'],
            self.params['droplet_lifetime'],
        ))

    def render(self):
        self.clear_brightness(0.4)
        self.zero_volume()

        for droplet in self.droplets:
            cx = int(droplet.x)
            cy = int(droplet.y)

            # Draw the wave

            r = droplet.radius()

            inner_r = r - droplet.thickness / 2
            outer_r = r + droplet.thickness / 2

            if inner_r > max(ARRAY_ROWS, ARRAY_COLUMNS):
                # None of the wave is visible
                continue

            left = int(max(cx - outer_r, 0))
            right = math.ceil(min(cx + outer_r, ARRAY_COLUMNS))
            top = int(max(cy - outer_r, 0))
            bottom = math.ceil(min(cy + outer_r, ARRAY_ROWS))

            for y in range(top, bottom):
                for x in range(left, right):
                    if not in_bounds(x, y):
                        # Skip out of bounds
                        continue

                    dist = distance(cx, cy, x, y)
                    if dist < inner_r or dist > outer_r:
                        continue

                    self.set_brightness(x, y, self.params['min_brightness'])

        for droplet in self.droplets:
            cx = int(droplet.x)
            cy = int(droplet.y)

            # Make the unit at the center loud and bright
            breathing_brightness = (1 + math.sin(2 * math.pi * self.time / self.params['breathing_period'])) / 2
            self.set_brightness(cx, cy, breathing_brightness)
            self.set_volume(cx, cy, 1)

    def update(self, dt):
        not_full = len(self.droplets) < self.params['max_units_active']
        if not_full and random.random() < self.params['chance_of_raindrop'] * dt:
            self.new_droplet()

        for droplet in self.droplets:
            droplet.update(dt)

        # Remove the dead droplets
        self.droplets = [p for p in self.droplets if p.alive]
