UNIT_COUNT = 180
ARRAY_COLUMNS = 13
ARRAY_ROWS = 14


class Behavior:
    def __init__(self, params):
        self.params = params

        self.brightness = [0] * UNIT_COUNT
        self.volume = [0] * UNIT_COUNT

        self.time = 0

    def update(self, dt):
        self.time += dt

        # Update effect/ sim state/etc.

    def render(self):
        # Should write any updates to self.brightness and self.volume
        pass
