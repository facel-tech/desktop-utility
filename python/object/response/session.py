from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from python.object.response.ping import Ping


class Session(BaseModel):
    start: datetime
    end: Optional[datetime]
    user_id: str
    id: str
    ping: Ping