from pydantic import BaseModel


class LocationResponse(BaseModel):
    ip: str
    country_code: str
    country_name: str
    region_code: str
    region_name: str
    city: str
    zip_code: str
    time_zone: str
    latitude: float
    longitude: float
