import os
import subprocess
import sys
import webbrowser

from python.constants.app import RANDOM_USER_ID, LOGGING_PATH
from python.constants.links import BUG_REPORT_SURVEY, CHANGELOG, APP_ITSELF, ABOUT_APP, AUTH_REQUEST
from python.utils.log import logger
from python.utils.mixpanel import mp


def on_send_bug_click():
    mp.track(RANDOM_USER_ID, "Sending bug report", {
        "type": "desktop"
    })

    webbrowser.open(BUG_REPORT_SURVEY)


def on_open_logs_click():
    mp.track(RANDOM_USER_ID, "Opening logs", {
        "type": "desktop"
    })

    if sys.platform != "win32":
        subprocess.call(['open', '-a', 'TextEdit', LOGGING_PATH])

    else:
        subprocess.call(["notepad.exe", LOGGING_PATH])


def on_update_click():
    mp.track(RANDOM_USER_ID, "Opening downloads", {
        "type": "desktop"
    })

    webbrowser.open(CHANGELOG)


def on_open_app_click(is_logged, request):
    if is_logged:
        mp.track(RANDOM_USER_ID, "Opening app in browser", {
            "type": "desktop"
        })

        webbrowser.open(APP_ITSELF)

    else:
        mp.track(RANDOM_USER_ID, "Opening login in browser", {
            "type": "desktop"
        })

        webbrowser.open(AUTH_REQUEST.format(request))


def on_manual_click():
    mp.track(RANDOM_USER_ID, "Opening about app", {
        "type": "desktop"
    })

    webbrowser.open(ABOUT_APP)


def on_close_app_click():
    logger.info("Closing app!")

    mp.track(RANDOM_USER_ID, "Killing app", {
        "type": "desktop"
    })

    os.system('kill %d' % os.getpid())
