from typing import Optional
from pydantic import BaseModel


class NextSendResponse(BaseModel):
    pause: int
    next: Optional[int]
