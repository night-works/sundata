import pytest
import pytest

from src.sundata import LightPeriod



@pytest.mark.parametrize("angles", [0, 1, 2, 3, 4, 10, 20, 30, 40, 50])
@pytest.mark.timeout(5)
def test_get_day(angles):
    assert LightPeriod.get(angles) == LightPeriod.DAY


@pytest.mark.parametrize("angles", [-0.0001, -1, -2, -3, -4, -5, -5.999999999, -6])
def test_get_civil(angles):
    assert LightPeriod.get(angles) == LightPeriod.CIVIL


@pytest.mark.parametrize("angles", [-6.00000001, -7, -8, -9, -10, -11, -11.999999999])
def test_get_nautiucal(angles):
    assert LightPeriod.get(angles) == LightPeriod.NAUTICAL


@pytest.mark.parametrize("angles", [-12.0000001, -13, -14, -15, -16, -17, -18])
def test_get_astro(angles):
    assert LightPeriod.get(angles) == LightPeriod.ASTRO


@pytest.mark.parametrize(
    "angles", [-18.0000001, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30]
)
def test_get_night(angles):
    assert LightPeriod.get(angles) == LightPeriod.NIGHT
