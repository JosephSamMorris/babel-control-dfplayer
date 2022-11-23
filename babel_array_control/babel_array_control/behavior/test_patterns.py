from .behavior import Behavior
from ..lights import UNIT_COUNT


class TestPatternsBehavior(Behavior):
    def __init__(self, params):
        super().__init__(params)

        # Create a checkerboard pattern
        self.brightness = [i % 2 == 0 for i in range(UNIT_COUNT)]
