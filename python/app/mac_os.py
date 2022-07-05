import os
import platform
import sys
import time
from threading import Thread

from PyQt6.QtWidgets import QMessageBox, QPushButton

from python.app.other import relaunch
from python.constants.app import RANDOM_USER_ID
from python.constants.pauses import PAUSE_EVALUATE_SYSTEM
from python.utils.log import logger
from packaging import version

from python.utils.mixpanel import mp

kIOHIDAccessTypeDenied = 1
kIOHIDAccessTypeGranted = 0
kIOHIDAccessTypeUnknown = 2
kIOHIDRequestTypeListenEvent = 1
kIOHIDRequestTypePostEvent = 0


def set_relaunch_message():
    msg = QMessageBox()

    msg.setText("If you already allowed Facel to read your keystrokes, please press the button below to refresh the app.")
    msg.setWindowTitle("Facel")

    button = QPushButton("Yes, relaunch")
    button.clicked.connect(relaunch)

    msg.setDefaultButton(button)
    msg.adjustSize()
    msg.exec()


def is_keyboard_verified(ioset):
    status = ioset['IOHIDCheckAccess'](kIOHIDRequestTypeListenEvent)
    logger.info("Keyboard verification status: {}".format(status))

    return status == kIOHIDAccessTypeGranted


def is_accessibility_verified():
    import HIServices
    return HIServices.AXIsProcessTrusted()


def is_should_check_input():
    return version.parse(platform.mac_ver()[0]) >= version.parse("10.15")


def run_input_checks(
    iterator,
    q_menu,
    q_action_input_monitor,
    ioset
):
    try:
        if iterator == PAUSE_EVALUATE_SYSTEM:
            return

        time.sleep(1)
        is_verified = is_keyboard_verified(ioset)
        logger.info("Is keyboard verified: {}".format(is_verified))

        if not is_verified:
            run_input_checks(
                iterator + 1,
                q_menu,
                q_action_input_monitor,
                ioset
            )
            return

        q_menu.removeAction(q_action_input_monitor)
        relaunch()

    except Exception as ex:
        logger.error(ex)


def run_accessibility_checks(
    iterator,
    q_menu,
    q_action_accessibility
):
    try:
        if iterator == PAUSE_EVALUATE_SYSTEM:
            return

        time.sleep(1)
        is_trusted = is_accessibility_verified()

        if not is_trusted:
            run_accessibility_checks(
                iterator + 1,
                q_menu,
                q_action_accessibility
            )
            return

        q_menu.removeAction(q_action_accessibility)
        relaunch()

    except Exception as ex:
        logger.error(ex)


def load_iot():
    try:
        import objc
        from Foundation import NSBundle
        IOKit = NSBundle.bundleWithIdentifier_('com.apple.framework.IOKit')

        ioset = {}
        functions = [
            ("IOHIDRequestAccess", b"BI"),
            ("IOHIDCheckAccess", b"II"),
        ]

        objc.loadBundleFunctions(IOKit, ioset, functions)

        return ioset

    except Exception as e:
        logger.error(e)


def on_accessibility_click(
        q_menu,
        q_action_accessibility
):
    try:
        import HIServices
        from ApplicationServices import kAXTrustedCheckOptionPrompt

        HIServices.AXIsProcessTrustedWithOptions({
            kAXTrustedCheckOptionPrompt: True
        })

        logger.info("Called accessibility")
        run_accessibility_checks(0, q_menu, q_action_accessibility)

    except Exception as ex:
        logger.error(ex)


def manual_request_input_access():
    try:
        from AppKit import NSWorkspace, NSURL

        url = "x-apple.systempreferences:com.apple.preference.security?Privacy_ListenEvent"
        url = NSURL.alloc().initWithString_(url)
        NSWorkspace.sharedWorkspace().openURL_(url)

    except Exception as e:
        logger.error(e)


def on_input_monitor_click(
        q_menu,
        q_action_input_monitor,
        ioset,
        is_iohid_dont_work
):
    try:
        result = ioset['IOHIDRequestAccess'](kIOHIDRequestTypeListenEvent)
        logger.info("Called IOHIDRequestAccess, result={}".format(result))

        if is_iohid_dont_work:
            manual_request_input_access()

        run_input_checks(
            0,
            q_menu,
            q_action_input_monitor,
            ioset
        )

    except Exception as e:
        logger.error(e)


def is_mac_os():
    return sys.platform == "darwin"


def check_mac_os_for_different_versions(
        q_menu,
        q_action_input_monitor,
        q_action_accessibility,
        is_manual,
        is_first_time
):
    try:
        if is_manual:
            mp.track(RANDOM_USER_ID, "Opening Mac OS permissions", {
                "type": "desktop"
            })

        logger.info("[CHECK] Loading IOT")
        ioset = load_iot()
        is_input_monitor_required = is_should_check_input()

        if is_input_monitor_required:
            logger.info("[CHECK] Input monitoring is required")
            logger.info("[CHECK] Removing q_action_accessibility from accessibility")

            q_menu.removeAction(q_action_accessibility)

            is_keyboard_ok = is_keyboard_verified(ioset)
            logger.info("[CHECK] Is keyboard trusted: {}".format(is_keyboard_ok))

            if not is_keyboard_ok:
                is_iohid_dont_work = (not is_first_time) or is_manual

                logger.info("Is first time: {}".format(is_first_time))
                logger.info("Is manual: {}".format(is_manual))

                thread = Thread(target=on_input_monitor_click, args=(
                    q_menu,
                    q_action_input_monitor,
                    ioset,
                    is_iohid_dont_work
                ))
                thread.start()

            else:
                logger.info("[CHECK] Is keyboard trusted: {}".format(is_keyboard_ok))
                q_menu.removeAction(q_action_input_monitor)

        else:
            logger.info("[CHECK] Removing q_action_input_monitor from accessibility")
            q_menu.removeAction(q_action_input_monitor)

            is_accessibility_ok = is_accessibility_verified()
            logger.info("[CHECK] Is accessibility trusted: {}".format(is_accessibility_ok))

            if not is_accessibility_ok:
                thread = Thread(target=on_accessibility_click, args=(
                    q_menu,
                    q_action_accessibility
                ))
                thread.start()

            else:
                q_menu.removeAction(q_action_accessibility)

    except Exception as e:
        logger.error(e)

    logger.info("[CHECK] Check is over")


