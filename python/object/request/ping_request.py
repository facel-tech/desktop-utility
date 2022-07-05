from pydantic import BaseModel


class PingRequest(BaseModel):
    timestamp: int
    session_id: str
    next_data_send: int
