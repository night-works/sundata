import astropy.coordinates as coord
from astropy.coordinates import AltAz, get_sun
from astropy.time import Time
import astropy.units as u
from datetime import datetime
from enum import Enum

from dataclasses import dataclass


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
    altazframe = AltAz(obstime=when, location=earth_location)
    sunaltaz = get_sun(when).transform_to(altazframe)
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
