from .behavior import Behavior
from ..lights import UNIT_COUNT
from .util import constrain


class Transition(Behavior):
    def __init__(self, from_behavior, to_behavior, transition_time=10):
        super().__init__({})

        self.from_behavior = from_behavior
        self.to_behavior = to_behavior
        self.transition_time = transition_time

        self.ratio_complete = 0

    def update(self, dt):
        super().update(dt)

        self.ratio_complete = constrain(self.time / self.transition_time, 0, 1)

        # Update the two behaviors that we are transitioning between

        if self.ratio_complete != 1:
            self.from_behavior.update(dt)

        if self.ratio_complete != 0:
            self.to_behavior.update(dt)

    def done(self):
        return self.ratio_complete >= 1


class FadeTransition(Transition):
    def render(self):
        self.from_behavior.render()
        self.to_behavior.render()

        for i in range(UNIT_COUNT):
            from_brightness = self.from_behavior.brightness[i]
            to_brightness = self.to_behavior.brightness[i]
            self.brightness[i] = from_brightness * (1 - self.ratio_complete) + to_brightness * self.ratio_complete

            from_volume = self.from_behavior.volume[i]
            to_volume = self.to_behavior.volume[i]
            self.volume[i] = from_volume * (1 - self.ratio_complete) + to_volume * self.ratio_complete
