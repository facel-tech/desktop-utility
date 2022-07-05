from datetime import datetime
from pydantic import BaseModel

from python.object.parameter.location_fixed_naming import LocationFixedNaming
from python.object.weather import Weather


class Geo(BaseModel):
    weather: Weather
    location: LocationFixedNaming
    ip: str
    session: str
    date: datetime