from sundata.sundata import Position, get_sun_altitude, lighting_is
from datetime import datetime


def test_get_altitude():
    pos = Position(51.772938, 0.102310)
    when = datetime(2023, 2, 12, 23, 3)
    assert get_sun_altitude(pos, when) == -49.20252290488592


def test_get_altitude_zero():
    pos = Position(51.772938, 0.102310)
    when = datetime(2023, 2, 12, 17, 3)
    sun = get_sun_altitude(pos, when)
    assert int(sun) == 0


def test_get_altitude_20():
    pos = Position(51.772938, 0.102310)
    when = datetime(2023, 2, 12, 19, 16)
    sun = get_sun_altitude(pos, when)
    assert int(sun) == -20


def test_get_light_period_day():
    pos = Position(51.772938, 0.102310)
    when = datetime(2023, 2, 12, 19, 16)
    sun = get_sun_altitude(pos, when)
    print(lighting_is(sun))