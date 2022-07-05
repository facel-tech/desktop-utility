from typing import Dict

from pydantic import BaseModel

from python.object.parameter.timing_features import TimingFeatures


class Timing(BaseModel):
    items: Dict[str, TimingFeatures]