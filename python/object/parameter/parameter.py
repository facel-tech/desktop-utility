from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from python.object.parameter.geo import GeoParameter
from python.object.parameter.keyboardparameter import KeyboardParameter
from python.object.parameter.mouseparameter import MouseParameter


class Parameter(BaseModel):
    user_id: str
    date: datetime
    length: int
    keyboard: Optional[KeyboardParameter]
    mouse: Optional[MouseParameter]
    geo: Optional[GeoParameter]
