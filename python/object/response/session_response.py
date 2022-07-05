from pydantic import BaseModel

from python.object.response.session import Session


class SessionResponse(BaseModel):
    code: str
    data: Session
