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
from .babel import BabelBehavior


DEFAULT_TRANSITION_TIME = 60 * 5


class BehaviorController:
    def __init__(self, array_server, rate=5):
        self.array_server = array_server
        self.update_thread = Thread(target=self.update_thread_fn, daemon=True)

        self.rate = rate

        self.weekday_active_from_hour = 15  # Turns on from this hour
        self.weekend_active_from_hour = 17
        self.active_to_hour = 22  # Turns off after this hour

        self.transitioning = False
        self.time_of_last_transition = None

        self.behaviors_by_name = {
            'babel': BabelBehavior(),
            'test_patterns': TestPatternsBehavior({}),
            'background': BackgroundBehavior(),
            'raindrops': RainDropsBehavior(),
            'wall_of_sound': WallOfSoundBehavior(),
            'musical': MusicalBehavior(),
            'wipe': WipeBehavior(),
            'sim_people': SimPeopleBehavior(),
        }

        self.behavior_rotation = [
            ('babel', 30),
            ('raindrops', DEFAULT_TRANSITION_TIME),
            ('babel', 30),
            ('musical', DEFAULT_TRANSITION_TIME),
            ('babel', 30),
            ('wipe', DEFAULT_TRANSITION_TIME),
        ]

        self.behavior_index = 0
        self.current_behavior = None
        self.next_behavior_name = None
        self.set_behavior('background')

    def set_behavior(self, behavior_name):
        if behavior_name not in self.behaviors_by_name:
            raise Exception('Unrecognized behavior name')

        self.current_behavior = self.behaviors_by_name[behavior_name]

    def transition_to(self, behavior_name):
        print(f'Transitioning to {behavior_name}')

        # Cancel any active transition
        if self.transitioning:
            self.current_behavior = self.current_behavior.to_behavior
            self.next_behavior_name = None
            self.transitioning = False

        self.current_behavior = FadeTransition(
            self.current_behavior,
            self.behaviors_by_name[behavior_name],
        )
        self.next_behavior_name = behavior_name

        self.transitioning = True

    def current_behavior_name(self):
        return self.behavior_rotation[self.behavior_index][0]

    def behavior_is_or_will_be(self, behavior_name):
        if self.transitioning:
            return self.next_behavior_name == behavior_name
        else:
            return self.current_behavior_name() == behavior_name

    def is_active(self):
        # Play the background behavior until it is late enough in the day

        datetime_now = datetime.datetime.now()
        is_weekday = datetime_now.weekday() < 5

        if is_weekday:
            active_from_hour = self.weekday_active_from_hour
        else:
            active_from_hour = self.weekend_active_from_hour

        return active_from_hour <= datetime_now.hour < self.active_to_hour

    def update_thread_fn(self):
        last_update_time = time.time()
        period = 1.0 / self.rate

        while True:
            now = time.time()
            dt = now - last_update_time
            last_update_time = now

            if not self.is_active():
                # Background behavior during inactive hours
                if not self.behavior_is_or_will_be('background'):
                    self.transition_to('background')
            else:
                # Cycle through our behaviors during active hours

                behavior_transition_time = DEFAULT_TRANSITION_TIME

                try:
                    behavior_transition_time = self.behavior_rotation[self.behavior_index][1]
                except ValueError:
                    # The current behavior is not in the rotation
                    pass

                if self.time_of_last_transition is None or now - self.time_of_last_transition > behavior_transition_time:
                    self.behavior_index += 1
                    self.behavior_index %= len(self.behavior_rotation)

                    self.transition_to(self.behavior_rotation[self.behavior_index][0])
                    self.time_of_last_transition = now

            if self.transitioning:
                if self.current_behavior.done():
                    # Must handle transition specially because
                    # we don't want to reset the behavior we are transitioning to
                    self.current_behavior = self.current_behavior.to_behavior
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
            time_until_next_update = max(period - time_spent_updating, 0)
            time.sleep(time_until_next_update)

    def start(self):
        self.update_thread.start()
