import time
import random
from .behavior import Behavior
from ..lights import in_bounds, unit_pos_from_index, ARRAY_ROWS, ARRAY_COLUMNS
from ..units_info import get_musical_units
from .util import distance


def near_others(unit, others, min_dist):
    x, y = unit_pos_from_index(unit)

    for other in others:
        ox, oy = unit_pos_from_index(other)
        dist = distance(x, y, ox, oy)

        # print(dist, min_dist, dist < min_dist)

        if dist < min_dist:
            return True

    return False


def find_distant_unit(all_units, avoid, min_dist, retries=100):
    for i in range(retries):
        selected_unit = random.choice(all_units)

        if not near_others(selected_unit, avoid, min_dist):
            return selected_unit

    # Try cycling through all of them one by one
    for selected_unit in all_units:
        if not near_others(selected_unit, avoid, min_dist):
            return selected_unit

    # Ok now we know there is not one that works
    return None


class MusicalBehavior(Behavior):
    def __init__(self):
        super().__init__({
            'num_to_highlight': 3,
            'min_distance': 5,
            'transition_delay': 30,  # How many seconds between switching highlighted units
        })

        self.musical_units = list(map(lambda info: info['index'], get_musical_units()))

        self.highlight_time = None
        self.highlighted = []

    def render(self):
        self.zero_brightness()
        self.zero_volume()

        for unit_index in self.highlighted:
            cx, cy = unit_pos_from_index(unit_index)

            self.set_volume(cx, cy, 1)

            self.set_brightness(cx - 1, cy, 1)
            self.set_brightness(cx + 1, cy, 1)
            self.set_brightness(cx, cy - 1, 1)
            self.set_brightness(cx, cy + 1, 1)

        return None

    def select_new_highlights(self, count):
        new_highlights = []

        for i in range(count):
            # If it's far enough away from the other units we have selected to highlight then we are done.
            # Might be None if we can't find one far enough away.
            selected_unit = find_distant_unit(self.musical_units, new_highlights, self.params['min_distance'])

            if selected_unit is None:
                # Skip because we couldn't find a unit far enough away
                continue

            new_highlights.append(selected_unit)

        self.highlighted = new_highlights

    def update(self, dt):
        now = time.time()

        if self.highlight_time is None or (now - self.highlight_time) > self.params['transition_delay']:
            self.select_new_highlights(self.params['num_to_highlight'])
            self.highlight_time = now
