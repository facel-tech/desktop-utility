import asyncio
from threading import Thread
import json
import sched
import threading
import time

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox, QMainWindow, QPushButton, QLabel
from PyQt6.QtGui import QIcon, QAction
import websockets
from python.app.other import create_resources
create_resources()

from python.app.other import set_unhandled_exceptions_handler, is_message_viewed, set_message_viewed
is_first_time = is_message_viewed()

from python.app.auth import get_auth, generate_random_auth_request, save_auth
from python.app.callbacks import on_open_app_click, on_manual_click, on_send_bug_click, on_update_click, \
    on_open_logs_click, on_close_app_click
from python.app.mac_os import is_mac_os, check_mac_os_for_different_versions
from python.constants.api import SOCKET_UPDATES_URL, SOCKET_WAITING_URL
from python.constants.app import RANDOM_USER_ID
from python.executors.updates import UpdatesExecutor
from python.executors.parameter import ParameterExecutor
from python.executors.session import SessionExecutor
from python.listeners.geo import GeoListener
from python.object.confidential_user_update_notification import ConfidentialUserUpdateNotification
from python.object.short_auth import ShortAuth
from python.object.update import DATA_SOURCES_CHANGED
from python.utils.mixpanel import mp
from python.utils.log import logger
from python.app.autorun import add_to_autostart
from python.constants.resources import POPUP_FIRST_LAUNCH, \
    SEND_BUG_REPORT, SHOW_LOGS, DOWNLOAD_NEW_VERSION, VERSION_TEXT, NOT_LOGGED_IN, LOG_IN, OPEN_APP, LOGGED_IN, \
    SUPPORT_GUIDE, KEYBOARD_DISABLED, KEYBOARD_ENABLED, ACCESSIBILITY_ALERT, INPUT_ALERT, QUIT, HAPPY_ICON, SAD_ICON

# adding app to launching together with system
logger.info("[BASE] Adding to autostart")
add_to_autostart()
logger.info(VERSION_TEXT)

# creating app
logger.info("[BASE] Creating app itself")
q_app = QApplication([])
q_app.setQuitOnLastWindowClosed(False)

# configuring executors and scheduling
logger.info("[BASE] Creating listeners")
listener = GeoListener()
parameter_executor = ParameterExecutor(listener)
session_executor = SessionExecutor(listener)
updates_executor = UpdatesExecutor()
parameter_executor.change_keyboard_listening(False)

# setting critical error handler
logger.info("[BASE] Setting exceptions handler")
set_unhandled_exceptions_handler(q_app)

# adding scheduler (single one)
logger.info("[BASE] Creating and setting scheduler")
scheduler = sched.scheduler(time.time, time.sleep)
parameter_executor.set_scheduler(scheduler)
session_executor.set_scheduler(scheduler)
updates_executor.set_scheduler(scheduler)

# adding resources
logger.info("[BASE] Creating buttons and icons")
q_tray_icon = QSystemTrayIcon()
q_icon_happy = QIcon(HAPPY_ICON)
q_icon_sad = QIcon(SAD_ICON)
q_menu = QMenu()
q_action_accessibility = QAction(ACCESSIBILITY_ALERT)
q_action_input_monitor = QAction(INPUT_ALERT)
q_action_keyboard = QAction(KEYBOARD_ENABLED)
q_action_web = QAction(LOG_IN)
q_action_manual = QAction(SUPPORT_GUIDE)
q_action_version = QAction(VERSION_TEXT)
q_action_report = QAction(SEND_BUG_REPORT)
q_action_logs = QAction(SHOW_LOGS)
q_action_quit = QAction(QUIT)
q_action_logged_in = QAction(NOT_LOGGED_IN)

# setting different stuff
logger.info("[BASE] Setting some buttons / icons")
q_tray_icon.setIcon(q_icon_happy)
q_tray_icon.setVisible(True)
q_action_version.setEnabled(False)
q_action_logged_in.setEnabled(False)

# adding actions
logger.info("[BASE] Adding buttons / icons to menu")
q_menu.addAction(q_action_input_monitor)
q_menu.addAction(q_action_accessibility)
q_menu.addAction(q_action_keyboard)
q_menu.addSeparator()
q_menu.addAction(q_action_logged_in)
q_menu.addAction(q_action_web)
q_menu.addAction(q_action_manual)
q_menu.addSeparator()
q_menu.addAction(q_action_version)
q_menu.addAction(q_action_report)
q_menu.addAction(q_action_logs)
q_menu.addSeparator()
q_menu.addAction(q_action_quit)

# initializing global scope
logger.info("[BASE] Initing global scope")
token, user_id = get_auth()
is_keyboard_enabled = True
is_last = True
generated_request = generate_random_auth_request()

mp.track(RANDOM_USER_ID, "Started desktop utility")


def set_hello_message():
    logger.info("[SET] In process of showing message")
    msg = QMessageBox()
    msg.setText(POPUP_FIRST_LAUNCH)
    msg.setWindowTitle("Facel")
    msg.adjustSize()
    msg.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
    msg.exec()
    logger.info("[SET] Message is shown")


def set_keyboard_button():
    logger.info("[SET] Keyboard button")

    if is_keyboard_enabled:
        q_action_keyboard.setText(KEYBOARD_ENABLED)
        q_tray_icon.setIcon(q_icon_happy)

    else:
        q_action_keyboard.setText(KEYBOARD_DISABLED)
        q_tray_icon.setIcon(q_icon_sad)


def set_version():
    logger.info("[SET] version")
    q_action_version.setEnabled(not is_last)

    if is_last:
        q_action_version.setText(VERSION_TEXT)

    else:
        q_action_version.setText(DOWNLOAD_NEW_VERSION)


def set_logged_in():
    logger.info("[SET] Logged in")

    mp.track(RANDOM_USER_ID, "Logged in session", {
        "type": "desktop"
    })

    q_action_logged_in.setText(LOGGED_IN)
    q_action_web.setText(OPEN_APP)


def callback_version_update(is_updated_last):
    global is_last
    is_last = is_updated_last
    set_version()


def run_scheduler():
    logger.info("[RUN] Scheduler")
    scheduler.run()


def on_update_arrived(data):
    logger.info("[ON] Update arrived")

    global is_keyboard_enabled

    data = ConfidentialUserUpdateNotification.parse_obj(data)
    logger.info("[ON] Update type: {}".format(data.update_type))

    if data.update_type == DATA_SOURCES_CHANGED:
        is_keyboard_enabled = data.update.sources.is_keyboard_enabled
        parameter_executor.change_keyboard_listening(is_keyboard_enabled)
        set_keyboard_button()


async def run_updates_websocket():
    logger.info("[RUN] Updates websocket")

    url = SOCKET_UPDATES_URL.format(token)

    async with websockets.connect(url) as websocket:
        while True:
            try:
                data = await websocket.recv()
                parsed = json.loads(data)
                on_update_arrived(parsed)

            except Exception as ex:
                logger.error(ex)


def run_create_api(is_already_running=False):
    logger.info("[RUN] Create API")

    global is_keyboard_enabled

    set_logged_in()

    parameter_executor.create_api(token, user_id)
    session_executor.create_api(token, user_id)

    logger.info("[RUN] Checking if keyboard is enabled")
    is_keyboard_enabled = session_executor.get_data_sources().is_keyboard_enabled
    parameter_executor.change_keyboard_listening(is_keyboard_enabled)
    set_keyboard_button()

    if not is_already_running:
        logger.info("[RUN] Asyncio is not running, so I'm running it")
        loop = asyncio.get_event_loop()
        loop.create_task(run_updates_websocket())
        thread = Thread(target=loop.run_forever)
        thread.start()

    else:
        logger.info("[RUN] Asyncio is running, so I'm just adding task")
        asyncio.create_task(run_updates_websocket())


def on_token_arrived(data):
    global token, user_id
    logger.info("[ON] Token arrived")

    data = ShortAuth.parse_obj(data)
    token = data.token
    user_id = data.user_id

    save_auth(user_id, token)
    run_create_api(is_already_running=True)


async def run_auth_waiting():
    logger.info("[RUN] Waiting till auth")
    url = SOCKET_WAITING_URL.format(generated_request)

    async with websockets.connect(url) as websocket:
        data = await websocket.recv()
        parsed = json.loads(data)
        on_token_arrived(parsed)


def on_keyboard_change_click():
    logger.info("[ON] Clicked on keyboard change")
    global is_keyboard_enabled
    is_keyboard_enabled = not is_keyboard_enabled

    mp.track(RANDOM_USER_ID, "Switching keyboard", {
        "value": "{} => {}".format(not is_keyboard_enabled, is_keyboard_enabled),
        "type": "desktop"
    })

    set_keyboard_button()
    parameter_executor.change_keyboard_listening(is_keyboard_enabled)
    session_executor.send_keyboard_enabled(is_keyboard_enabled)


def is_logged_in():
    return token is not None


def run_check_mac_os_for_different_versions(is_manual):
    logger.info("[RUN] Checking Mac OS permissions")

    try:
        thread = Thread(target=check_mac_os_for_different_versions, args=(
            q_menu,
            q_action_input_monitor,
            q_action_accessibility,
            is_manual,
            is_first_time
        ))

        thread.start()

    except Exception as e:
        logger.error(e)


if is_mac_os():
    logger.info("[BASE] Platform is MacOS, I'm checking the permissions")
    run_check_mac_os_for_different_versions(False)


if is_first_time:
    logger.info("[BASE] First time around")
    set_message_viewed()
    logger.info("[BASE] Showing hello message")
    set_hello_message()


if is_logged_in():
    try:
        logger.info("[BASE] Creating API, because user passed auth")
        mp.alias(RANDOM_USER_ID, user_id)
        run_create_api(is_already_running=False)

    except Exception as e:
        logger.error(e)
        token = None
        user_id = None

else:
    logger.info("[BASE] Running checks for authorization")
    loop = asyncio.get_event_loop()
    logger.info("[BASE] Adding task to asyncio on auth waiting")
    loop.create_task(run_auth_waiting())
    logger.info("[BASE] Running asyncio loop")
    thread = Thread(target=loop.run_forever)
    thread.start()


# starting constant checks
logger.info("[BASE] Running scheduler")
thread_scheduler = threading.Thread(target=run_scheduler)
thread_scheduler.start()

# setting up updater
logger.info("[BASE] Setting updates callback")
updates_executor.set_callback(callback_version_update)
updates_executor.run()

# initializing button listeners
logger.info("[BASE] Setting button triggers")
q_action_web.triggered.connect(lambda: on_open_app_click(
    is_logged=is_logged_in(),
    request=generated_request
))
q_action_accessibility.triggered.connect(lambda: run_check_mac_os_for_different_versions(True))
q_action_input_monitor.triggered.connect(lambda: run_check_mac_os_for_different_versions(True))
q_action_keyboard.triggered.connect(on_keyboard_change_click)
q_action_manual.triggered.connect(on_manual_click)
q_action_report.triggered.connect(on_send_bug_click)
q_action_logs.triggered.connect(on_open_logs_click)
q_action_quit.triggered.connect(on_close_app_click)
q_action_version.triggered.connect(on_update_click)

# starting app
logger.info("[BASE] Starting app")
q_tray_icon.setContextMenu(q_menu)
q_app.exec()
