from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

import astropy.coordinates as coord
import astropy.units as u
from astropy.time import Time


@dataclass
class Position:
    latitude: float
    longitude: float


class LightPeriod(Enum):
    NIGHT = 0
    ASTRO = 1
    NAUTICAL = 2
    CIVIL = 3
    DAY = 4


def get_sun_altitude(position: Position, when: datetime) -> float:
    earth_location = coord.EarthLocation(
        lon=position.longitude * u.deg, lat=position.latitude * u.deg
    )
    when = Time(when, format="datetime", scale="utc")
    altazframe = coord.AltAz(obstime=when, location=earth_location)
    sunaltaz = coord.get_sun(when).transform_to(altazframe)
    return sunaltaz.alt.max().value


def lighting_is(sun_altitude: float) -> LightPeriod:
    if sun_altitude >= 0:
        return LightPeriod.DAY
    if sun_altitude < -18:
        return LightPeriod.NIGHT
    if sun_altitude < 0 and sun_altitude >= -6:
        return LightPeriod.CIVIL
    if sun_altitude < -6 and sun_altitude >= -12:
        return LightPeriod.NAUTICAL
    if sun_altitude < -12 and sun_altitude >= -18:
        return LightPeriod.ASTRO


def get_lighting_period_after(
    position: Position, when: datetime, period: LightPeriod
) -> datetime:
    lighting = when

    while period.value != lighting_is(get_sun_altitude(position, lighting)).value:
        lighting = lighting + timedelta(minutes=1)

    return lighting


def get_lighting_period_before(
    position: Position, when: datetime, period: LightPeriod
) -> datetime:
    lighting = when

    while period.value != lighting_is(get_sun_altitude(position, lighting)).value:
        lighting = lighting - timedelta(minutes=1)

    return lighting
