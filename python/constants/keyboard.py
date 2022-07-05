from enum import Enum

KEY = "key"
TIME = "timestamp"
TYPE = "type"
PRESS_TIME = "press"
RELEASE_TIME = "release"
DIFFERENCE = "difference"


class ActionType(Enum):
    RELEASE = 1
    PRESS = 0

PR = "pr"
RP = "rp"
RR = "rr"
PP = "pp"
PRPR = "prpr"

FEATURES = (
    PR,
    RP,
    RR,
    PP,
    PRPR
)
