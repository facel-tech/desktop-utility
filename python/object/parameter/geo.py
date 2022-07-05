from typing import Optional

from pydantic import BaseModel

from python.object.parameter.time_features import TimeFeatures


class GeoParameter(BaseModel):
    time: Optional[TimeFeatures]