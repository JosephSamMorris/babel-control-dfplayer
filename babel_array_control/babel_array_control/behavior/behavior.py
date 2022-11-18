from ..lights import unit_index_from_pos, UNIT_COUNT


class Behavior:
    def __init__(self, params):
        self.params = params

        self.brightness = [0] * UNIT_COUNT
        self.volume = [0] * UNIT_COUNT

        self.time = 0

    def zero_brightness(self):
        self.brightness = [0] * UNIT_COUNT

    def zero_volume(self):
        self.volume = [0] * UNIT_COUNT

    def set_brightness(self, x, y, brightness):
        index = unit_index_from_pos(x, y)
        self.brightness[index] = brightness

    def set_volume(self, x, y, volume):
        index = unit_index_from_pos(x, y)
        self.volume[index] = volume

    def update(self, dt):
        self.time += dt

        # Update effect/sim state/etc.

    def render(self):
        # Should write any updates to self.brightness and self.volume
        pass
