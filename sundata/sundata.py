import astropy.coordinates as coord
from astropy.coordinates import AltAz,get_sun
from astropy.time import Time
import astropy.units as u
from datetime import datetime

from dataclasses import dataclass

@dataclass
class Position:
    latitude:float
    longitude:float


def get_sun_altitude(position:Position, when:datetime) -> float:
    earth_location = coord.EarthLocation(lon=position.longitude * u.deg,
                          lat=position.latitude * u.deg)
    when = Time(when, format='datetime', scale='utc')                                  
    altazframe = AltAz(obstime=when, location=earth_location)                                               
    sunaltaz = get_sun(when).transform_to(altazframe)  
    return sunaltaz.alt.max().value
    
