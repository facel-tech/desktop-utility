import json
from datetime import datetime
import logging
from threading import Thread

from uplink.auth import BearerToken
from python.api.geo import GeoService
from python.api.location import LocationService
from python.api.main import MainGateService
from python.constants.api import BASE_URL
from python.constants.app import VERSION, APP_TYPE, DEFAULT_LOGGER
from python.constants.pauses import PAUSE_PING
from python.object.geo import Geo
from python.object.request.create_session_request import CreateSessionRequest
from python.object.request.data_source_request import SetParticularDataSourceRequest
from python.object.request.geo_request import GeoRequest
from python.object.request.ping_request import PingRequest


class SessionExecutor:
    def __init__(self, geo_listener):
        self.main_api = None
        self.geo_api = GeoService()
        self.location_api = None
        self.user_id = None

        self.session = None
        self.scheduler = None
        self.geo_listener = geo_listener

        self.logger = logging.getLogger(DEFAULT_LOGGER)

    def create_session(self):
        try:
            request = CreateSessionRequest(
                version=VERSION,
                app=APP_TYPE
            )

            thing = json.loads(request.json())
            self.session = self.main_api.create_session(thing).data

        except Exception as e:
            self.logger.error(e)

    def create_api(self, token, user_id):
        if self.main_api is not None:
            return

        self.logger.info("Creating API")
        bearer = BearerToken(token)
        self.main_api = MainGateService(base_url=BASE_URL, auth=bearer)
        self.location_api = LocationService(base_url=BASE_URL, auth=bearer)
        self.user_id = user_id

        self.logger.info("Creating session object")
        self.create_session()
        self.ping()

        thread = Thread(target=self.send_location)
        thread.start()

    def recreate_api(self, token, user_id):
        self.main_api = None
        self.create_api(token, user_id)

    def send_keyboard_enabled(self, is_keyboard_enabled):
        request = SetParticularDataSourceRequest(is_keyboard_enabled=is_keyboard_enabled)
        thing = json.loads(request.json())
        self.logger.info("Sending SetDataSource request")

        if self.main_api is not None:
            self.main_api.set_particular_data_source(thing)

    def set_scheduler(self, scheduler):
        self.scheduler = scheduler

    def get_next_data_send(self, scheduler):
        nearest_execute = None

        for event in scheduler.queue:
            if event.action.__name__ == "execute":
                nearest_execute = event.time * 1000
                break

        return nearest_execute

    def get_data_sources(self):
        return self.main_api.get_data_sources().data

    def ping(self):
        try:
            if self.main_api is not None:
                next_data_send = self.get_next_data_send(self.scheduler)

                request = PingRequest(
                    timestamp=round(datetime.now().timestamp()),
                    session_id=self.session.id,
                    next_data_send=next_data_send
                )

                thing = json.loads(request.json())
                self.logger.info("Pinging session")
                self.main_api.ping_session(thing)

        except Exception as e:
            self.logger.error(e)

        self.scheduler.enter(PAUSE_PING, 1, self.ping)

    def send_location(self):
        location, ip = self.geo_listener.get_geo()
        weather = self.geo_api.get_weather_info(location.lat, location.lon)

        request = GeoRequest(
            geo=Geo(
                weather=weather,
                location=location,
                ip=ip,
                session=self.session.id,
                date=datetime.now()
            )
        )

        thing = json.loads(request.json())

        self.logger.info("Sending location")

        if self.location_api is not None:
            self.location_api.add_location(thing)
