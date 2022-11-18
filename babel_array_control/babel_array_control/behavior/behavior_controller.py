import time
import json
from threading import Thread
from .sim_people import SimPeopleBehavior
from .raindrops import RainDropsBehavior


class BehaviorController:
    def __init__(self, array_server, rate=5):
        self.array_server = array_server
        self.update_thread = Thread(target=self.update_thread_fn, daemon=True)

        self.rate = rate
        self.behaviors_by_name = {
            # 'sim_people': SimPeopleBehavior(),
            'raindrops': RainDropsBehavior(),
        }

        if len(self.behaviors_by_name) > 0:
            self.current_behavior = self.behaviors_by_name[next(iter(self.behaviors_by_name))]
        else:
            self.current_behavior = None

    def set_behavior(self, behavior_name):
        if behavior_name in self.behaviors_by_name:
            raise Exception('Unrecognized behavior name')

        self.current_behavior = self.behaviors_by_name[behavior_name]

    def update_thread_fn(self):
        last_update_time = time.time()
        period = 1.0 / self.rate

        while True:
            now = time.time()
            dt = now - last_update_time
            last_update_time = now

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
