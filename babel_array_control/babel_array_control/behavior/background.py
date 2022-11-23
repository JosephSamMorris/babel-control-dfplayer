from .behavior import Behavior
from ..lights import unit_index_from_pos, ARRAY_ROWS, ARRAY_COLUMNS
from .util import constrain
import perlin

noise = perlin.Perlin(824393)


class BackgroundBehavior(Behavior):
    def __init__(self):
        super().__init__({
            'min_brightness': 0.2,
            'max_brightness': 1,
        })

    def render(self):
        self.zero_volume()

        for y in range(ARRAY_ROWS):
            for x in range(ARRAY_COLUMNS):
                idx = unit_index_from_pos(x, y)

                if idx is None:
                    continue

                prl = noise.three(x * 100, y * 300, self.time * 300 + 10)
                b = (1 - constrain(-prl, 0, 20) / 20) * (self.params['max_brightness'] - self.params['min_brightness']) + self.params['min_brightness']

                self.brightness[idx] = b
