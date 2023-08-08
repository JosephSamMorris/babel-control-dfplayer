from freezegun import freeze_time
from babel_array_control.server import ArrayServer
from babel_array_control.behavior import BehaviorController

def test_active_hours():
    array_server = ArrayServer()
    behavior_controller = BehaviorController(array_server)

    # 4-24 is a Monday
    # 4-30 is a Sunday

    # Weekday hours
    # Mon: 8am-10pm!
    # Tuesday - Weds - Thurs - Fri: 8am-3pm

    # NOT active at 7:59 AM on Monday
    with freeze_time('2023-04-24 07:59:00'):
        assert not behavior_controller.is_active()

    # NOT active at 10:01 PM on Monday
    with freeze_time('2023-04-24 22:01:00'):
        assert not behavior_controller.is_active()

    # NOT active at 7:59 AM on Tuesday
    with freeze_time('2023-04-25 07:59:00'):
        assert not behavior_controller.is_active()

    # ACTIVE at 8:01 AM on Wednesday
    with freeze_time('2023-04-26 08:01:00'):
        assert behavior_controller.is_active()

    # ACTIVE at 2:59 PM on Thursday
    with freeze_time('2023-04-27 14:59:00'):
        assert behavior_controller.is_active()

    # NOT active at 3:01 PM on Thursday
    with freeze_time('2023-04-27 15:01:00'):
        assert not behavior_controller.is_active()

    # Sat - Sun: 5pm-10pm

    # NOT active at 4:59 PM on Saturday
    with freeze_time('2023-04-29 16:59:00'):
        assert not behavior_controller.is_active()

    # ACTIVE at 5:01 PM on Saturday
    with freeze_time('2023-04-29 17:01:00'):
        assert behavior_controller.is_active()

    # ACTIVE at 9:59 PM on Saturday
    with freeze_time('2023-04-29 21:59:00'):
        assert behavior_controller.is_active()

    # NOT active at 10:01 PM on Saturday
    with freeze_time('2023-04-29 22:01:00'):
        assert not behavior_controller.is_active()
