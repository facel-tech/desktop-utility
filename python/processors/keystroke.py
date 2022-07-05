import logging
import re
from typing import Optional
import pandas as pd

from python.constants.app import DEFAULT_LOGGER
from python.constants.keyboard import KEY, TYPE, ActionType
from python.constants.keystrokes import BACKSPACE, DELETE, END, ARROWS, HOME, ENDINGS, PUNCTUATIONS, TABS, UPPERCASE, \
    CTRL, INSERTS, RETURNS, SHIFT, SPACES, NUMBERS, LOWERCASE
from python.object.parameter.keystroke_rates import KeystrokeRates


def get_rate(table, length, key):
    if length == 0:
        return 0

    fixed = map(lambda x: re.escape(x), key)
    key = "|".join(fixed)

    symbols = table[table[KEY].str.contains(key, na=False)]
    return round(len(symbols) / length, 6)


class KeystrokesProcessor:
    def __init__(self):
        self.logger = logging.getLogger(DEFAULT_LOGGER)

    def process(self, vector) -> Optional[KeystrokeRates]:
        try:
            table = pd.DataFrame(vector)
            table = table[table[TYPE] == ActionType.PRESS]
            table = table[~table[KEY].str.contains("None", na=False)]
            self.logger.info("Processing keystrokes, totally {}".format(len(table)))

            length = len(table)

            backspaces_rate = get_rate(table, length, BACKSPACE)
            delete_rate = get_rate(table, length, DELETE)
            end_rate = get_rate(table, length, END)

            arrow_rate = get_rate(table, length, ARROWS)
            home_rate = get_rate(table, length, HOME)
            ending_rate = get_rate(table, length, ENDINGS)

            punctuation_rate = get_rate(table, length, PUNCTUATIONS)
            tab_rate = get_rate(table, length, TABS)
            caps_rate = get_rate(table, length, UPPERCASE)
            ctrl_rate = get_rate(table, length, CTRL)
            insert_rate = get_rate(table, length, INSERTS)
            return_rate = get_rate(table, length, RETURNS)
            shift_rate = get_rate(table, length, SHIFT)
            space_rate = get_rate(table, length, SPACES)
            other_rate = get_rate(table, length, NUMBERS + LOWERCASE)

            return KeystrokeRates(
                backspace=backspaces_rate,
                delete=delete_rate,
                end=end_rate,
                arrow=arrow_rate,
                home=home_rate,
                sentence_ending=ending_rate,
                punctuation=punctuation_rate,
                tab=tab_rate,
                caps=caps_rate,
                control=ctrl_rate,
                insert=insert_rate,
                return_r=return_rate,
                shift=shift_rate,
                space=space_rate,
                other=other_rate,
                size=length
            )

        except Exception as e:
            self.logger.error(e, stack_info=True)
            return None
