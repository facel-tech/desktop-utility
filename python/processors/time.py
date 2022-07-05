import logging
from typing import Optional
from astral.sun import sun
from astral import LocationInfo
from datetime import datetime

from python.constants.app import DEFAULT_LOGGER
from python.constants.time import DAWN, LOWER_LIMIT, NOON, DUSK
from python.object.parameter.time_features import TimeFeatures


class TimeProcessor:
    def __init__(self):
        self.logger = logging.getLogger(DEFAULT_LOGGER)

    def get_sun_features(self, location: LocationInfo, time: datetime) -> float:
        sun_instance = sun(location.observer, date=time.date())

        dawn = sun_instance[DAWN]
        noon = sun_instance[NOON]
        dusk = sun_instance[DUSK]

        time = datetime.now(dawn.tzinfo)

        if time < dawn or time > dusk:
            return LOWER_LIMIT

        if time <= noon:
            big_difference = (noon - dawn).seconds
            small_difference = (time - dawn).seconds
            return small_difference / big_difference

        else:
            big_difference = (dusk - noon).seconds
            small_difference = (time - noon).seconds
            return 1 - (small_difference / big_difference)

    def process(self, vector) -> Optional[TimeFeatures]:
        try:
            lat = vector.lat
            lng = vector.lon

            location = LocationInfo(
                latitude=lat,
                longitude=lng
            )

            time = datetime.now()
            sun = self.get_sun_features(location, time)
            self.logger.info("Feature: {}".format(sun))

            return TimeFeatures(
                sun=round(sun, 7)
            )

        except Exception as e:
            self.logger.error(e)
            return None


