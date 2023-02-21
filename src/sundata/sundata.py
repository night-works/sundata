from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

import pytz
from astropy import coordinates
from astropy import units
from astropy.time import Time
from suntime import Sun


@dataclass
class Position:
    latitude: float
    longitude: float


class LightPeriod(Enum):
    NIGHT = (-18.0000000001, -200.0)
    ASTRO = (-12.0000001, -18)
    NAUTICAL = (-6.00000001, -11.999999999)
    CIVIL = (-0.0000001, -6)
    DAY = (0, 200)

    @staticmethod
    def get(value: float):
        for data in LightPeriod:
            low = data.value[0]
            high = data.value[1]
            if low >= value >= high:
                return data
        return LightPeriod.DAY


class LightingInformation:
    sunrise: datetime
    sunset: datetime
    location: Position
    set_date: datetime
    utc = pytz.UTC

    def __init__(self, position: Position, a_datetime: datetime) -> None:
        self.location = position
        self.set_date = a_datetime.astimezone(self.utc)

    def calculate(self, lighting_period: LightPeriod = LightPeriod.DAY):
        sun = Sun(self.location.latitude, self.location.longitude)
        self.sunrise = sun.get_local_sunrise_time(self.set_date).astimezone(self.utc)
        sunrise_angle = get_sun_altitude(self.location, self.sunrise)
        if sunrise_angle < 0 and lighting_period == LightPeriod.DAY:
            self.sunrise = get_lighting_period_after(
                self.location, self.sunrise, lighting_period
            )
        else:
            self.sunrise = get_lighting_period_before(
                self.location, self.sunrise, lighting_period
            )

        self.sunset = sun.get_local_sunset_time(self.set_date).astimezone(self.utc)
        sunset_angle = get_sun_altitude(self.location, self.sunset)

        if sunset_angle < 0 and lighting_period == LightPeriod.DAY:
            self.sunset = get_lighting_period_before(
                self.location, self.sunset, lighting_period
            )
        else:
            self.sunset = get_lighting_period_after(
                self.location, self.sunset, lighting_period
            )


def get_sun_altitude(position: Position, when: datetime) -> float:
    earth_location = coordinates.EarthLocation(
        lon=position.longitude * units.deg, lat=position.latitude * units.deg
    )
    when = Time(when, format="datetime", scale="utc")
    alt_frame = coordinates.AltAz(obstime=when, location=earth_location)
    sun_alt = coordinates.get_sun(when).transform_to(alt_frame)
    return sun_alt.alt.max().value


def get_lighting_period_after(position: Position, when: datetime, period: LightPeriod) -> datetime:
    lighting = when

    while period != LightPeriod.get(get_sun_altitude(position, lighting)):
        lighting = lighting + timedelta(minutes=1)

    return lighting


def get_lighting_period_before(position: Position, when: datetime, period: LightPeriod) -> datetime:
    lighting = when

    while period != LightPeriod.get(get_sun_altitude(position, lighting)):
        lighting = lighting - timedelta(minutes=1)

    return lighting
