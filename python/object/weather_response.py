from pydantic import BaseModel

from python.object.current_weather import CurrentWeather
from python.object.weather import Weather


class WeatherResponse(BaseModel):
    latitude: float
    longitude: float
    hourly: Weather
    utc_offset_seconds: int
    elevation: float
    generationtime_ms: float
    current_weather: CurrentWeather
