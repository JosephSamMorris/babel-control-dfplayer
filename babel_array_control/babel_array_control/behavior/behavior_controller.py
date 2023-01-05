import time
import json
import datetime
from threading import Thread
from .test_patterns import TestPatternsBehavior
from .background import BackgroundBehavior
from .transitions import FadeTransition
from .raindrops import RainDropsBehavior
from .wall_of_sound import WallOfSoundBehavior
from .sim_people import SimPeopleBehavior
from .musical import MusicalBehavior
from .wipe import WipeBehavior


class BehaviorController:
    def __init__(self, array_server, rate=5):
        self.array_server = array_server
        self.update_thread = Thread(target=self.update_thread_fn, daemon=True)

        self.rate = rate

        self.active_from_hour = 15  # Turns on from this hour
        self.active_to_hour = 22  # Turns off after this hour

        self.transition_period = 60 * 5
        self.transitioning = False
        self.time_of_last_transition = None

        self.behaviors_by_name = {
            'test_patterns': TestPatternsBehavior({}),
            'background': BackgroundBehavior(),
            'raindrops': RainDropsBehavior(),
            'wall_of_sound': WallOfSoundBehavior(),
            'musical': MusicalBehavior(),
            'wipe': WipeBehavior(),
            'sim_people': SimPeopleBehavior(),
        }

        self.behavior_rotation = [
            'raindrops',
            'musical',
            'wipe',
        ]

        self.current_behavior = None
        self.current_behavior_name = None
        self.next_behavior_name = None
        self.set_behavior('background')

    def set_behavior(self, behavior_name):
        if behavior_name not in self.behaviors_by_name:
            raise Exception('Unrecognized behavior name')

        self.current_behavior = self.behaviors_by_name[behavior_name]
        self.current_behavior_name = behavior_name

    def transition_to(self, behavior_name):
        print(f'Transitioning to {behavior_name}')

        self.current_behavior = FadeTransition(
            self.current_behavior,
            self.behaviors_by_name[behavior_name],
        )
        self.next_behavior_name = behavior_name

        self.transitioning = True

    def behavior_is_or_will_be(self, behavior_name):
        if self.transitioning:
            return self.next_behavior_name == behavior_name
        else:
            return self.current_behavior_name == behavior_name

    def update_thread_fn(self):
        last_update_time = time.time()
        period = 1.0 / self.rate

        while True:
            now = time.time()
            dt = now - last_update_time
            last_update_time = now

            # Play the background behavior until it is late enough in the day
            datetime_now = datetime.datetime.now()
            if datetime_now.hour < self.active_from_hour or datetime_now.hour >= self.active_to_hour:
                if not self.behavior_is_or_will_be('background'):
                    self.transition_to('background')
            else:
                # Cycle the behaviors periodically
                if self.time_of_last_transition is None or now - self.time_of_last_transition > self.transition_period:
                    if self.current_behavior_name is not None:
                        try:
                            behavior_index = self.behavior_rotation.index(self.current_behavior_name)
                            behavior_index += 1
                            behavior_index %= len(self.behavior_rotation)
                        except ValueError:
                            behavior_index = 0
                    else:
                        behavior_index = 0

                    self.transition_to(self.behavior_rotation[behavior_index])
                    self.time_of_last_transition = now

            if self.transitioning:
                if self.current_behavior.done():
                    # Must handle transition specially because
                    # we don't want to reset the behavior we are transitioning to
                    self.current_behavior = self.current_behavior.to_behavior
                    self.current_behavior_name = self.next_behavior_name
                    self.next_behavior_name = None
                    self.transitioning = False

            if self.current_behavior is not None:
                self.current_behavior.update(dt)
                self.current_behavior.render()

                cmd = json.dumps({
                    'command': 'blit',
                    'brightness': self.current_behavior.brightness,
                    'volume': self.current_behavior.volume,
                })
                self.array_server.handle_behavior_request(cmd)

            time_spent_updating = time.time() - last_update_time
            time_until_next_update = period - time_spent_updating
            time.sleep(time_until_next_update)

    def start(self):
        self.update_thread.start()
