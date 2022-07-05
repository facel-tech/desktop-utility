from enum import Enum
from typing import Optional
from pydantic import BaseModel
from python.object.sources import CombinedDataSource

USER_OFFLINE = "USER_OFFLINE"
USER_ONLINE = "USER_ONLINE"
USER_STEALTH_START = "USER_STEALTH_START"
USER_STEALTH_STOP = "USER_STEALTH_STOP"
DATA_SOURCES_CHANGED = "DATA_SOURCES_CHANGED"


class Update(BaseModel):
    id: str
    sources: Optional[CombinedDataSource]