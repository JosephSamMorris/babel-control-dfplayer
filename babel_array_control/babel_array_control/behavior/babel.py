from .behavior import Behavior


class BabelBehavior(Behavior):
    def __init__(self):
        super().__init__({})

    def render(self):
        self.clear_volume(1)
        self.clear_brightness(1)
