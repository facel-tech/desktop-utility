from pydantic import BaseModel


class MeanStd(BaseModel):
    mean: float
    std: float
    size: int