import json
import os
import secrets
from os import path

from python.constants.app import COOK
from python.constants.auth import USER_ID, TOKEN
from python.utils.log import logger


def get_auth():
    if path.exists(COOK):
        with open(COOK) as f:
            content = json.load(f)

            if TOKEN in content:
                token = content[TOKEN]
                user_id = content[USER_ID]
                return token, user_id

    return None, None


def generate_random_auth_request():
    return secrets.token_urlsafe(16)


def save_auth(user_id, token):
    try:
        try:
            os.makedirs(os.path.dirname(COOK))

        except Exception as e:
            logger.error(e)

        with open(COOK, "w+") as f:
            content = {
                TOKEN: token,
                USER_ID: user_id
            }

            json.dump(content, f)
            f.close()

    except Exception as ex:
        logger.error(ex)
