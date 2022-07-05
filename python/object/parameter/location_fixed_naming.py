from pydantic import BaseModel


class LocationFixedNaming(BaseModel):
    status: str
    country: str
    country_code: str
    region: str
    region_name: str
    city: str
    zip: str
    lat: float
    lon: float
    timezone: str
    isp: str
    org: str
