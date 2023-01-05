from babel_array_control.lights import unit_pos_from_index, unit_index_from_pos, ARRAY_COLUMNS, ARRAY_ROWS


def test_unit_pos_from_index():
    # Units are 0-indexed
    assert unit_pos_from_index(0) == (0, 0)

    assert unit_pos_from_index(20) == (7, 1)

    # The first one after the first 6 full rows is after the gap where the bar is
    assert unit_pos_from_index(ARRAY_COLUMNS * 6) == (2, 6)

    # The next gap row
    assert unit_pos_from_index(ARRAY_COLUMNS * 6 + 11) == (2, 7)

    # The last one
    assert unit_pos_from_index(ARRAY_COLUMNS * 12 + (ARRAY_COLUMNS - 2) * 2 - 1) == (12, 13)


def test_unit_index_from_pos():
    # Out of bounds should return None
    assert unit_index_from_pos(-20, 0) is None
    assert unit_index_from_pos(0, -20) is None
    assert unit_index_from_pos(20, 0) is None
    assert unit_index_from_pos(0, 20) is None

    # First
    assert unit_index_from_pos(0, 0) == 0

    # Last
    assert unit_index_from_pos(12, 13) == 177

    # Middle ones from each section
    assert unit_index_from_pos(7, 4) == 4 * 13 + 7
    assert unit_index_from_pos(9, 7) == 6 * 13 + 11 + (9 - 2)
    assert unit_index_from_pos(2, 11) == 6 * 13 + 2 * 11 + 3 * 13 + 2


def test_coordinates_to_from_index():
    for y in range(ARRAY_ROWS):
        for x in range(ARRAY_COLUMNS):
            if (y == 6 or y == 7) and (x == 0 or x == 1):
                # Skip the bar
                continue

            assert unit_index_from_pos(x, y) is not None
