from python.api.geo import GeoService


class GeoListener:
    def __init__(self):
        self.api = GeoService()
        self.place = None
        self.ip = None

    def get_geo(self):
        if self.place is None:
            # just getting geolocation using IP
            self.place, self.ip = self.api.get_location_info()

        return self.place, self.ip


