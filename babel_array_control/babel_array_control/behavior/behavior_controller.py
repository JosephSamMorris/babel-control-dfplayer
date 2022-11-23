import time
import json
from threading import Thread
from .test_patterns import TestPatternsBehavior
from .background import BackgroundBehavior
from .transitions import FadeTransition
from .raindrops import RainDropsBehavior
from .wall_of_sound import WallOfSoundBehavior
from .sim_people import SimPeopleBehavior
from .musical import MusicalBehavior


class BehaviorController:
    def __init__(self, array_server, randomize_behavior=False, rate=5):
        self.array_server = array_server
        self.update_thread = Thread(target=self.update_thread_fn, daemon=True)

        self.rate = rate
        self.transitioning = False
        self.behaviors_by_name = {
            'test_patterns': TestPatternsBehavior({}),
            'background': BackgroundBehavior(),
            'raindrops': RainDropsBehavior(),
            'wall_of_sound': WallOfSoundBehavior(),
            'musical': MusicalBehavior(),
            'sim_people': SimPeopleBehavior(),
        }

        self.behavior_rotation = [
            # 'background',
            # 'raindrops',
            'musical',
        ]

        self.current_behavior = None
        self.set_behavior(self.behavior_rotation[0])

    def set_behavior(self, behavior_name):
        if behavior_name not in self.behaviors_by_name:
            raise Exception('Unrecognized behavior name')

        self.current_behavior = self.behaviors_by_name[behavior_name]

    def transition_to(self, behavior_name):
        self.current_behavior = FadeTransition(
            self.current_behavior,
            self.behaviors_by_name[behavior_name],
        )

        self.transitioning = True

    def update_thread_fn(self):
        last_update_time = time.time()
        period = 1.0 / self.rate

        while True:
            now = time.time()
            dt = now - last_update_time
            last_update_time = now

            if self.transitioning:
                if self.current_behavior.done():
                    self.current_behavior = self.current_behavior.to_behavior
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
