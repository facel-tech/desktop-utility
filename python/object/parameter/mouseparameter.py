from typing import Optional

from pydantic import BaseModel

from python.object.parameter.mean_std import MeanStd


class MouseParameter(BaseModel):
    press_release: Optional[MeanStd]