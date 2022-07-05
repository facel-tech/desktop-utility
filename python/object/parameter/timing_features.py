from pydantic import BaseModel

from python.object.parameter.mean_std import MeanStd


class TimingFeatures(BaseModel):
    pr: MeanStd
    rp: MeanStd
    prpr: MeanStd
    rr: MeanStd
    pp: MeanStd