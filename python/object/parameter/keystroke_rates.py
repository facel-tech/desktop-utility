from pydantic import BaseModel


class KeystrokeRates(BaseModel):
    backspace: float
    delete: float
    end: float
    arrow: float
    home: float
    sentence_ending: float
    punctuation: float
    tab: float
    caps: float
    control: float
    insert: float
    return_r: float
    shift: float
    space: float
    other: float
    size: int