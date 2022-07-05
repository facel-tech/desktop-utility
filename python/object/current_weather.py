from datetime import datetime

from pydantic import BaseModel


class CurrentWeather(BaseModel):
    temperature: float
    weathercode: int
    windspeed: float
    winddirection: int
    time: datetime