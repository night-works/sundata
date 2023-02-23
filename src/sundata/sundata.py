from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Tuple

import pytz
from astropy import coordinates
from astropy import units
from astropy.time import Time
from suntime import Sun


@dataclass
class Position:
    """
    Represents a location on Earth surface as a latitude and longitude
    """
    latitude: float
    longitude: float


class LightPeriod(Enum):
    f"""
    An {Enum} that represents the various lighting scenarios during a day.
    """
    NIGHT = (-18.0000000001, -200.0)
    ASTRO = (-12.0000001, -18)
    NAUTICAL = (-6.00000001, -11.999999999)
    CIVIL = (-0.0000001, -6)
    DAY = (0, 200)

    @staticmethod
    def get(value: float):
        f"""
        Get the {LightPeriod} that the {float} falls within otherwise {LightPeriod.DAY} is returned
        
        Args:
            value:  a {float} representation of an altitude

        Returns: the {LightPeriod} that the {float} falls within otherwise {LightPeriod.DAY} is returned

        """
        for data in LightPeriod:
            low = data.value[0]
            high = data.value[1]
            if low >= value >= high:
                return data
        return LightPeriod.DAY


class SunData:
    f"""
    For a give {Position} and {datetime} calculate the sunrise and sunset {datetime} allowing for the shift of those 
    to other lighting scenarios for example get the time when the sun would be entering {LightPeriod.CIVIL}
    """
    sunrise: datetime
    sunset: datetime
    location: Position
    set_date: datetime
    utc = pytz.UTC

    def __init__(self, position: Position, a_datetime: datetime) -> None:
        f"""
        {SunData} constructor for the required information to calculate the sunrise and sunset with various
        lighting scenarios {LightPeriod}
       
        Args:
            position: a {Position} on the earth to base calculations from
            a_datetime: a fixed {datetime} to use for the basis of further calculations
        """
        self.location = position
        self.set_date = a_datetime.astimezone(self.utc)

    def calculate_sun_data(self, lighting_period: LightPeriod = LightPeriod.DAY) -> Tuple[datetime, datetime]:
        f"""
        Perform the calculations and modifications of the sunrise and sunset for a given optional {LightPeriod} if no 
        {LightPeriod} is provided then the default of {LightPeriod.DAY} is used which would result in the standard 
        definition of sunrise and sunset for the position on the Earth of the provided date.
        
        Args:
            lighting_period:

        Returns: {Tuple} of calculated Sunrise and Sunset as {datetime} objects

        """
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

        return self.sunrise, self.sunset


def get_sun_altitude(position: Position, a_datetime: datetime) -> float:
    f"""
    For a give {Position} and a {datetime} calculate the altitude of the Sun relative to the Earth Horizon. Note that a
    negative number will mean that the sun is below the Horizon, this is represented as a {float}
    
    Args:
        position: location on the earth with a latitude and longitude {Position}
        a_datetime: the {datetime} to get the sun altitude from

    Returns: the altitude {float} of the sun position relative to the horizon negative numbers are below horizon

    """
    latitude = position.latitude * units.deg
    longitude = position.longitude * units.deg
    earth_location = coordinates.EarthLocation(lon=longitude, lat=latitude)
    a_datetime = Time(a_datetime, format="datetime", scale="utc")
    alt_frame = coordinates.AltAz(obstime=a_datetime, location=earth_location)
    sun_alt = coordinates.get_sun(a_datetime).transform_to(alt_frame)
    return sun_alt.alt.max().value


def get_lighting_period_after(position: Position, a_datetime: datetime, period: LightPeriod) -> datetime:
    f"""
    Find the start of the next {LightPeriod} after the passed {datetime}. If the {datetime} is currently within the 
    requested {LightPeriod} then returns with current {datetime}
    
    Args:
        position: location on the earth with a latitude and longitude {Position}
        a_datetime: the {datetime} to get the sun altitude from
        period:

    Returns: the {datetime} of when the requested {LightPeriod} starts after the given {Position} and {datetime}

    """
    while period != LightPeriod.get(get_sun_altitude(position, a_datetime)):
        a_datetime = a_datetime + timedelta(minutes=1)

    return a_datetime


def get_lighting_period_before(position: Position, a_datetime: datetime, period: LightPeriod) -> datetime:
    f"""
    Find the start of the next {LightPeriod} before the passed {datetime}. If the {datetime} is currently within the 
    requested {LightPeriod} then returns with current {datetime}
        
    Args:
        position: location on the earth with a latitude and longitude {Position}
        a_datetime: the {datetime} to get the sun altitude from
        period: the {LightPeriod} to seek

    Returns: the {datetime} of when the requested {LightPeriod} ends after the given {Position} and {datetime}

    """
    while period != LightPeriod.get(get_sun_altitude(position, a_datetime)):
        a_datetime = a_datetime - timedelta(minutes=1)

    return a_datetime
