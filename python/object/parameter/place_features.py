from pydantic import BaseModel


class PlaceFeatures(BaseModel):
    lat: float
    lng: float
    city: str
    country: str