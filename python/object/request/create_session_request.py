from pydantic import BaseModel


class CreateSessionRequest(BaseModel):
    app: str
    version: str
