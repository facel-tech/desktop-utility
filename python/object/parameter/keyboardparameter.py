from typing import Optional

from pydantic import BaseModel

from python.object.parameter.keystroke_rates import KeystrokeRates
from python.object.parameter.timing import Timing


class KeyboardParameter(BaseModel):
    timing: Optional[Timing]
    keystroke: Optional[KeystrokeRates]