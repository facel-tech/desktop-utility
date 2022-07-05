from pydantic import BaseModel


class ShortAuth(BaseModel):
    request: str
    token: str
    user_id: str
