import logging
import time
from pynput import keyboard

from python.constants.app import DEFAULT_LOGGER
from python.constants.keyboard import KEY, TIME, TYPE, ActionType


class KeyboardListener:

    def __init__(self):
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )

        self.listener.start()

        self.is_started = False
        self.vector = []
        self.logger = logging.getLogger(DEFAULT_LOGGER)

    def write_to_database(self, key, type):
        if not self.is_started:
            return

        thing = {
            KEY: key,
            TIME: int(time.time_ns() / 1_000_000),
            TYPE: type
        }

        self.vector.append(thing)

    def on_press(self, key):
        try:
            thing = key.char

        except AttributeError:
            thing = str(key)

        if thing is None:
            thing = "None"

        self.write_to_database(thing, ActionType.PRESS)

    def on_release(self, key):
        try:
            thing = key.char

        except AttributeError:
            thing = str(key)

        if thing is None:
            thing = "None"

        self.write_to_database(thing, ActionType.RELEASE)

    def start(self):
        self.logger.info("Called keyboard start, current state is {}".format(self.is_started))

        try:
            if not self.is_started:
                self.is_started = True
                self.logger.info("Started keyboard listener!")

        except Exception as ex:
            self.logger.error(ex)

    def stop(self):
        self.logger.info("Called keyboard stop, current state is {}".format(self.is_started))

        try:
            if self.is_started:
                self.is_started = False
                self.logger.info("Stopped keyboard listener!")

        except Exception as ex:
            self.logger.error(ex)

    def get_data(self):
        vector = self.vector.copy()
        self.vector = []
        return vector
