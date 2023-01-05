from .behavior import Behavior
from ..lights import ARRAY_COLUMNS, ARRAY_ROWS
from .util import constrain


class WipeBehavior(Behavior):
    def __init__(self):
        super().__init__({
            'move_delay': 7,
        })

    def render(self):
        self.zero_volume()
        self.clear_brightness(0.1)

        wall_y = (self.time / self.params['move_delay']) % ARRAY_ROWS

        for y in range(ARRAY_ROWS):
            for x in range(ARRAY_COLUMNS):
                dist = abs(y - wall_y)
                norm_dist = dist / 2
                val = 1 - constrain(norm_dist, 0, 1)

                self.set_brightness(x, y, val)
                self.set_volume(x, y, val)

