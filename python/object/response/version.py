from datetime import datetime

from pydantic import BaseModel


class Version(BaseModel):
    code: str
    date: datetime
    url: str
    expiry_time: datetime