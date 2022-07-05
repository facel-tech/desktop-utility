from datetime import datetime
import logging
from uplink.auth import BearerToken
import json
from python.api.parameter import ParameterService
from python.constants.api import BASE_URL
from python.constants.app import DEFAULT_LOGGER
from python.constants.pauses import PAUSE_SEND
from python.listeners.keyboard import KeyboardListener
from python.listeners.mouse import MouseListener
from python.object.parameter.geo import GeoParameter
from python.object.parameter.keyboardparameter import KeyboardParameter
from python.object.parameter.parameter import Parameter
from python.processors.time import TimeProcessor
from python.processors.keystroke import KeystrokesProcessor
from python.processors.timing import TimingProcessor
from python.processors.mouse import MouseProcessor


class ParameterExecutor:
    def __init__(self, geo_listener):
        self.scheduler = None
        self.user_id = None
        self.parameter_api = None

        self.logger = logging.getLogger(DEFAULT_LOGGER)
        self.geo_listener = geo_listener

        self.keyboard_listener = KeyboardListener()
        self.mouse_listener = MouseListener()

        self.keystrokes_processor = KeystrokesProcessor()
        self.timing_processor = TimingProcessor()
        self.mouse_processor = MouseProcessor()
        self.time_processor = TimeProcessor()

        self.geo_listener.get_geo()

    def set_scheduler(self, scheduler):
        self.scheduler = scheduler
        self.logger.info("Starting scheduling parameters")
        self.scheduler.enter(PAUSE_SEND, 1, self.execute)

    def create_api(self, token, user_id):
        if self.parameter_api is not None:
            return

        self.user_id = user_id
        self.logger.info("Creating API")

        bearer = BearerToken(token)
        self.parameter_api = ParameterService(base_url=BASE_URL, auth=bearer)

    def recreate_api(self, token, user_id):
        self.parameter_api = None
        self.create_api(token, user_id)

    def get_keyboard(self, vector):
        if vector is None:
            return None

        if len(vector) != 0:
            timing = self.timing_processor.process(vector)
            keystroke = self.keystrokes_processor.process(vector)

            return KeyboardParameter(
                timing=timing,
                keystroke=keystroke
            )

        else:
            return None

    def get_geo(self, vector):
        if vector is not None:
            time = self.time_processor.process(vector)

            return GeoParameter(
                time=time
            )

        else:
            return None

    def get_mouse(self, vector):
        if vector is None:
            return None

        if len(vector) != 0:
            return self.mouse_processor.process(vector)

        else:
            return None

    def execute(self):
        try:
            if self.parameter_api is not None:
                self.logger.info("Sending parameter")

                geo_data, ip = self.geo_listener.get_geo()
                mouse_data = self.mouse_listener.get_data()
                keyboard_data = self.keyboard_listener.get_data()
                geo = self.get_geo(geo_data)
                keyboard = self.get_keyboard(keyboard_data)
                mouse = self.get_mouse(mouse_data)

                parameter = Parameter(
                    user_id=self.user_id,
                    date=datetime.now(),
                    length=PAUSE_SEND * 1000,
                    keyboard=keyboard,
                    mouse=mouse,
                    geo=geo
                )

                # for some reason applying a hack
                thing = json.loads(parameter.json())
                self.logger.info(thing)

                self.parameter_api.add_parameter(thing)
                self.geo_listener.get_geo()

        except Exception as e:
            self.logger.error(e)

        self.scheduler.enter(PAUSE_SEND, 1, self.execute)

    def change_keyboard_listening(self, is_enabled):
        try:
            self.logger.info("Changing keyboard listening from {} to {}".format(not is_enabled, is_enabled))

            if is_enabled:
                self.keyboard_listener.start()
                self.mouse_listener.start()

            else:
                self.keyboard_listener.stop()
                self.keyboard_listener.stop()

        except Exception as ex:
            self.logger.error(ex)
