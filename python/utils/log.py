import logging

from python.constants.app import DEFAULT_LOGGER, LOGGING_PATH
from python.utils.formatter import CustomFormatter

logger = logging.getLogger(DEFAULT_LOGGER)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)
fh = logging.FileHandler(LOGGING_PATH)
fh.setLevel(logging.NOTSET)
fh.setFormatter(CustomFormatter())
logger.addHandler(fh)