import logging
import time
from pynput import mouse

from python.constants.app import DEFAULT_LOGGER
from python.constants.mouse import TYPE, Y, X, TIME, MouseActionType


class MouseListener:

    def __init__(self):
        self.vector = []

        # initializing listener
        self.listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll
        )

        # we're starting right away, because we cannot call stop() and start() afterwards (it will crash this lib)
        self.listener.start()

        # getting default logger to log errors and stuff
        self.logger = logging.getLogger(DEFAULT_LOGGER)

        # listener is not started
        self.is_started = False

    def write_to_database(self, x, y, type):
        # if we've not started listener, we don't store anything
        if not self.is_started:
            return

        # computing timestamp of event
        exact_time = int(time.time_ns() / 1_000_000)

        thing = {
            X: x,
            Y: y,
            TYPE: type,
            TIME: exact_time
        }

        # adding to vector (NOTE: this is stored in memory, not on disk)
        self.vector.append(thing)

    def on_move(self, x, y):
        # in case person moved a cursor, we add this event
        self.write_to_database(x, y, MouseActionType.MOVE)

    def on_click(self, x, y, button, pressed):
        # in case person clicked, we add this
        type = MouseActionType.CLICK_PRESS if pressed else MouseActionType.CLICK_RELEASE
        self.write_to_database(x, y, type)

    def on_scroll(self, x, y, dx, dy):
        # in case person scrolled, we add this
        self.write_to_database(x, y, MouseActionType.SCROLL)

    def start(self):
        # starting listening
        self.logger.info("Called mouse start, current state is {}".format(self.is_started))

        try:
            if not self.is_started:
                self.logger.info("Started mouse listener!")
                self.is_started = True

        except Exception as e:
            self.logger.error(e)

    def stop(self):
        # stopping listening
        self.logger.info("Called mouse stop, current state is {}".format(self.is_started))

        try:
            if self.is_started:
                self.logger.info("Stopped mouse listener!")
                self.is_started = False

        except Exception as e:
            self.logger.error(e)

    def get_data(self):
        # returning data somewhere and reiniting
        vector = self.vector.copy()
        self.vector = []
        return vector
