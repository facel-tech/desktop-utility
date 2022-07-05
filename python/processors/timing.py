import logging
from typing import Optional
import pandas as pd
import numpy as np

from python.constants.app import DEFAULT_LOGGER
from python.constants.keyboard import KEY, TYPE, TIME, PRESS_TIME, RELEASE_TIME, DIFFERENCE, PRPR, PP, RR, RP, PR, \
    FEATURES, ActionType
from python.object.parameter.mean_std import MeanStd
from python.object.parameter.timing import Timing
from python.object.parameter.timing_features import TimingFeatures


def get_another_form(table):
    vector = []

    for key in table[KEY].unique():
        frame_by_key = table[table[KEY] == key]

        for i in range(len(frame_by_key) - 1):
            current = frame_by_key.iloc[i]
            next_one = frame_by_key.iloc[i + 1]

            if (current[TYPE] != ActionType.PRESS) and (next_one[TYPE] != ActionType.RELEASE):
                continue

            press = current[TIME]
            release = next_one[TIME]

            vector.append({
                PRESS_TIME: press,
                RELEASE_TIME: release,
                KEY: key
            })

    new_form = pd.DataFrame(vector)
    new_form = new_form.sort_values(by=PRESS_TIME)

    return new_form


def get_arrays_of_combinations(frame):
    output = {}

    for i in range(len(frame) - 1):
        first = frame.iloc[i]
        second = frame.iloc[i + 1]

        combination = first[KEY].lower() + "_" + second[KEY].lower()
        pr = second[PRESS_TIME] - first[RELEASE_TIME]
        rp = second[RELEASE_TIME] - first[PRESS_TIME]
        rr = second[RELEASE_TIME] - first[RELEASE_TIME]
        pp = second[PRESS_TIME] - first[PRESS_TIME]
        prpr = first[RELEASE_TIME] - first[PRESS_TIME] + second[RELEASE_TIME] - second[PRESS_TIME]

        if combination not in output:
            output[combination] = {i: [] for i in FEATURES}

        output[combination][PR].append(pr)
        output[combination][RP].append(rp)
        output[combination][RR].append(rr)
        output[combination][PP].append(pp)
        output[combination][PRPR].append(prpr)

    return output


def get_final_thing(output):
    final = {}

    for combination in output.keys():
        item = output[combination]
        features = {i: None for i in FEATURES}

        for feature in item.keys():
            values = np.array(item[feature])
            mean = values.mean()
            std = values.std()
            size = len(values)

            features[feature] = MeanStd(
                mean=mean,
                std=std,
                size=size
            )

        features = TimingFeatures.parse_obj(features)
        final[combination] = features

    return final


class TimingProcessor:
    def __init__(self):
        self.logger = logging.getLogger(DEFAULT_LOGGER)

    def process(self, vector) -> Optional[Timing]:
        try:
            table = pd.DataFrame(vector)
            self.logger.info("Processing timing, totally {}".format(len(table)))

            frame = get_another_form(table)
            frame[DIFFERENCE] = frame[RELEASE_TIME] - frame[PRESS_TIME]
            frame = frame[frame[DIFFERENCE] < 5 * 1_000]

            output = get_arrays_of_combinations(frame)
            final = get_final_thing(output)

            return Timing(
                items=final
            )

        except Exception as e:
            self.logger.error(e)
            return None
