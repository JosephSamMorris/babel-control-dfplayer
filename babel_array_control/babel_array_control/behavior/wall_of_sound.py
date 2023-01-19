import math
import perlin
from .behavior import Behavior
from ..lights import in_bounds, unit_index_from_pos, ARRAY_ROWS, ARRAY_COLUMNS
from .util import constrain
from ..units_info import get_units_by_priority

noise = perlin.Perlin(824393)


class WallOfSoundBehavior(Behavior):
    def __init__(self):
        super().__init__({
            'speed': 3,
            'light_wall_thickness': 3,
            'sound_wall_thickness': 5,
            'units_to_disable': get_units_by_priority(0),
        })

    def render(self):
        time_for_wall = ARRAY_ROWS / self.params['speed']
        time_for_transition = time_for_wall
        total_animation_time = time_for_wall + time_for_transition
        fade_to_brightness = 0.2

        # Time that loops
        anim_time = self.time % total_animation_time

        was_wall = True

        for y in range(ARRAY_ROWS):
            for x in range(ARRAY_COLUMNS):
                if not in_bounds(x, y):
                    continue

                idx = unit_index_from_pos(x, y)
                brightness_here = self.brightness[idx]
                volume_here = 0 if idx in self.params['units_to_disable'] else self.volume[idx]

                if anim_time > time_for_wall:
                    if was_wall:
                        self.zero_brightness()
                        was_wall = False

                    if volume_here > 0:
                        self.set_volume(x, y, volume_here * 0.3)

                    # Fade to black and then to full brightness and back to zero
                    transition_time = anim_time - time_for_wall
                    portion_complete = transition_time / time_for_transition

                    if portion_complete < 1 / 3:
                        piece = portion_complete / (1 / 3)

                        # Getting dimmer
                        self.set_brightness(x, y, (1 - piece) * fade_to_brightness)
                    elif 1 / 3 <= portion_complete < 2 / 3:
                        piece = (portion_complete - 1 / 3) / (1 / 3)

                        # Getting brighter
                        self.set_brightness(x, y, piece)
                    else:
                        piece = (portion_complete - 2 / 3) / (1 / 3)

                        # Getting dimmer
                        self.set_brightness(x, y, 1 - piece)

                    continue

                # Animate the wall

                if not was_wall:
                    self.zero_brightness()
                    was_wall = True

                brightness_here = self.brightness[idx]
                volume_here = self.volume[idx]

                wall_position = anim_time / time_for_wall * ARRAY_ROWS

                if brightness_here > 0.2:
                    self.set_brightness(x, y, brightness_here * 0.7)
                elif brightness_here > 0:
                    self.set_brightness(x, y, constrain(-noise.three(x * 500, y * 500, self.time * 100) / 20, 0.1, 0.2))

                if volume_here > 0.2:
                    self.set_volume(x, y, volume_here * 0.3)

                # Light wall
                dist_to_wall = abs(y - wall_position)
                if dist_to_wall < self.params['light_wall_thickness'] / 2:
                    # 0 to 1 going away from center
                    norm_dist = dist_to_wall / self.params['light_wall_thickness'] / 2
                    self.set_brightness(x, y, 1 - norm_dist)

                # Sound wall is full brightness
                dist_to_wall = abs(y - wall_position)
                if dist_to_wall < self.params['sound_wall_thickness'] / 2:
                    self.set_volume(x, y, 1)
