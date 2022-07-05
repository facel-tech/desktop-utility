from pydantic import BaseModel


class Ping(BaseModel):
    last_timestamp: int
    pings_count: int
    pings_mean: float