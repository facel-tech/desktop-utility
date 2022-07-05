from enum import Enum

TIME = "TIME"
X = "X"
Y = "Y"
TYPE = "TYPE"


class MouseActionType(Enum):
    MOVE = 1
    CLICK_PRESS = 2
    SCROLL = 3
    CLICK_RELEASE = 4
