from .behavior import Behavior
from ..lights import ARRAY_COLUMNS, ARRAY_ROWS


# Based on https://stackoverflow.com/a/398302
def spiral_xy(spiral_index, spacing=1):
    x = 0
    y = 0

    dx = 0
    dy = -1

    for i in range(spiral_index):
        if x == y or (x < 0 and x == -y) or (x > 0 and x == spacing - y):
            dx, dy = -dy, dx

        x, y = x + dx, y + dy

    return x, y


class SpiralBehavior(Behavior):
    def __init__(self):
        super().__init__({
            'move_delay': .1,
            'padding': 1,  # Space between the lines
            'spacing': 1,  # Space between one moving highlight and the next
        })

    def render(self):
        self.zero_volume()
        self.zero_brightness()

        time_index = int(self.time // self.params['move_delay'])
        offset = time_index % self.params['spacing']

        for i in range(offset, time_index + offset + 1, self.params['spacing']):
            sx, sy = spiral_xy(i, self.params['padding'])
            x = int(sx + ARRAY_COLUMNS / 2)
            y = int(sy + ARRAY_ROWS / 2)

            self.set_brightness(x, y, 1)
            self.set_volume(x, y, 1)
