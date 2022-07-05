import logging
from typing import Optional
import pandas as pd
import numpy as np

from python.constants.app import DEFAULT_LOGGER
from python.constants.keyboard import KEY, DIFFERENCE
from python.constants.mouse import TYPE, TIME, MouseActionType
from python.object.parameter.mean_std import MeanStd
from python.object.parameter.mouseparameter import MouseParameter


class MouseProcessor:
    def __init__(self):
        self.logger = logging.getLogger(DEFAULT_LOGGER)

    def process(self, vector) -> Optional[MouseParameter]:
        try:
            processed = []

            for i in range(0, len(vector) - 1):
                current = vector[i]
                next = vector[i + 1]

                processed.append({
                    KEY: str(current[TYPE]) + "_" + str(next[TYPE]),
                    DIFFERENCE: next[TIME] - current[TIME]
                })

            mouse = pd.DataFrame(processed)
            click_release = mouse[mouse[KEY] == "{}_{}".format(
                MouseActionType.CLICK_PRESS,
                MouseActionType.CLICK_RELEASE
            )]

            click_release = click_release.dropna()

            # less than 3 seconds
            click_release = click_release[click_release[DIFFERENCE] < 3_000]
            mean = np.mean(click_release[DIFFERENCE])
            std = np.std(click_release[DIFFERENCE])

            if len(click_release) == 0:
                return None

            return MouseParameter(
                press_release=MeanStd(
                    mean=round(mean, 6),
                    std=round(std, 6),
                    size=len(click_release)
                )
            )

        except Exception as e:
            self.logger.error(e)
            return None

