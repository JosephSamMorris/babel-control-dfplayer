from freezegun import freeze_time
from babel_array_control.server import ArrayServer
from babel_array_control.behavior import BehaviorController

def test_active_hours():
    array_server = ArrayServer()
    behavior_controller = BehaviorController(array_server)

    # Monday 4-24
    # Sunday 4-30

    # Weekday hours

    with freeze_time('2023-04-24 14:59:00'):
        # NOT active at 2:59 PM on Monday
        assert not behavior_controller.is_active()

    with freeze_time('2023-04-25 22:01:00'):
        # NOT active at 10:01 PM on Tuesday
        assert not behavior_controller.is_active()

    with freeze_time('2023-04-26 15:01:00'):
        # ACTIVE at 3:01 PM on Wednesday
        assert behavior_controller.is_active()

    with freeze_time('2023-04-26 21:59:00'):
        # ACTIVE at 9:59 PM on Wednesday
        assert behavior_controller.is_active()

    # Weekend hours are between 5 PM and 10 PM

    with freeze_time('2023-04-29 16:59:00'):
        # NOT active at 4:59 PM on Saturday
        assert not behavior_controller.is_active()

    with freeze_time('2023-04-30 22:01:00'):
        # NOT active at 10:01 PM on Sunday
        assert not behavior_controller.is_active()

    with freeze_time('2023-04-29 17:01:00'):
        # ACTIVE at 5:01 PM on Saturday
        assert behavior_controller.is_active()

    with freeze_time('2023-04-30 21:59:00'):
        # ACTIVE at 9:59 PM on Sunday
        assert behavior_controller.is_active()
