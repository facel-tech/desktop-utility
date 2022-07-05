import logging
import sys
from threading import Thread

from python.api.app import AppGateService
from python.constants.api import BASE_URL
from python.constants.app import VERSION, DEFAULT_LOGGER
from python.constants.pauses import PAUSE_UPDATE
from python.utils.log import logger


class UpdatesExecutor:
    def __init__(self):
        self.scheduler = None
        self.logger = logging.getLogger(DEFAULT_LOGGER)
        self.callback = None
        self.api = AppGateService(base_url=BASE_URL)

    def set_scheduler(self, scheduler):
        self.scheduler = scheduler
        self.logger.info("Starting scheduling parameters")
        self.scheduler.enter(PAUSE_UPDATE, 1, self.execute)

    def run(self):
        thread = Thread(target=self.execute)
        thread.start()

    def set_callback(self, callback):
        self.callback = callback

    def execute(self):
        try:
            logger.info("Checking version updates")
            response = self.api.check_if_last_desktop_utility(VERSION, sys.platform)
            is_last = response.data.is_last
            self.callback(is_last)

        except Exception as e:
            logger.error(e)
