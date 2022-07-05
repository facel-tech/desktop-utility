import requests

from python.constants.geo import FEATURES, GEO_API, IP_API, WEATHER_API
from python.object.parameter.location import Location
from python.object.parameter.location_fixed_naming import LocationFixedNaming
from python.object.weather import Weather
from python.object.weather_response import WeatherResponse


class GeoService:

    def get_location_info(self):
        ip_request = requests.get(IP_API)
        ip = ip_request.json()["ip"]

        geo_request = requests.get(GEO_API.format(ip))
        geo = geo_request.json()
        location = Location.parse_obj(geo)
        fixed = LocationFixedNaming(
            status=location.status,
            country=location.country,
            country_code=location.countryCode,
            region=location.region,
            region_name=location.regionName,
            city=location.city,
            zip=location.zip,
            lat=location.lat,
            lon=location.lon,
            timezone=location.timezone,
            isp=location.isp,
            org=location.org
        )

        return fixed, ip

    def get_weather_info(self, lat, lng) -> Weather:
        weather_request = requests.get(WEATHER_API.format(lat, lng, ",".join(FEATURES)))
        weather = weather_request.json()

        return WeatherResponse.parse_obj(weather).hourly
