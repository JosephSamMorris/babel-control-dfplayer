import math
import random
from ..lights import unit_pos_from_index


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def constrain(v, v_min, v_max):
    if v < v_min:
        return v_min
    elif v > v_max:
        return v_max

    return v


def near_others(unit, others, min_dist):
    x, y = unit_pos_from_index(unit)

    for other in others:
        ox, oy = unit_pos_from_index(other)
        dist = distance(x, y, ox, oy)

        # print(dist, min_dist, dist < min_dist)

        if dist < min_dist:
            return True

    return False


def find_distant_unit(all_units, avoid, min_dist, retries=10):
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
