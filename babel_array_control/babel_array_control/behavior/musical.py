import time
import math
from .behavior import Behavior
from ..lights import unit_pos_from_index
from ..units_info import get_musical_units
from .util import find_distant_unit, constrain


class MusicalBehavior(Behavior):
    def __init__(self):
        super().__init__({
            'num_to_highlight': 3,
            'min_brightness': 0.1,
            'min_distance': 5,
            'fade_in_time': 3,
            'breathing_period': 6,
            'transition_delay': 30,  # How many seconds between switching highlighted units
        })

        self.musical_units = list(map(lambda info: info['index'], get_musical_units()))

        self.highlight_time = None
        self.highlighted = []

    def render(self):
        self.clear_brightness(self.params['min_brightness'])
        self.zero_volume()

        for unit_index in self.highlighted:
            cx, cy = unit_pos_from_index(unit_index)

            volume_fade_in = constrain((time.time() - self.highlight_time) / self.params['fade_in_time'], 0, 1)
            self.set_volume(cx, cy, volume_fade_in)

            min_b = self.params['min_brightness']
            bp = self.params['breathing_period']
            breathing_brightness = min_b + 0.9 * (1 + math.sin(2 * math.pi * self.time / bp)) / 2
            self.set_brightness(cx, cy, breathing_brightness)

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
        super().update(dt)

        now = time.time()

        if self.highlight_time is None or (now - self.highlight_time) > self.params['transition_delay']:
            self.select_new_highlights(self.params['num_to_highlight'])
            self.highlight_time = now
