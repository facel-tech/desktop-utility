from pydantic import BaseModel

from python.object.geo import Geo


class GeoRequest(BaseModel):
    geo: Geo
