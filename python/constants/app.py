import os
from uuid import getnode as get_mac

VERSION = "1.3.7"
APP_TYPE = "DESKTOP_UTILITY"
RANDOM_USER_ID = '%012x' % get_mac()

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))) + "/Resources/"
COOK = BASE_PATH + "cook.json"
LOGGING_PATH = BASE_PATH + "logging.txt"
CRASH_PATH = BASE_PATH + "crash.txt"
MESSAGE_PATH = BASE_PATH + "message.json"

DEFAULT_LOGGER = "facel"
