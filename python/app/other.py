import os
import sys
import os.path
import traceback
from PyQt6.QtWidgets import QMessageBox
from python.constants.app import BASE_PATH, CRASH_PATH, LOGGING_PATH, MESSAGE_PATH


def create_resources():
    try:
        os.makedirs(os.path.dirname(BASE_PATH))
    except Exception as e:
        print(e)

    return os.path.isfile(LOGGING_PATH)


def is_message_viewed():
    print("Is message file: {}".format(os.path.isfile(MESSAGE_PATH)))
    return not os.path.isfile(MESSAGE_PATH)


def set_message_viewed():
    with open(MESSAGE_PATH, "w+") as f:
        f.write("{'viewed': true}")
        f.close()

def relaunch():
    os.system('kill %d' % os.getpid() + " && open -a Facel")

def set_unhandled_exceptions_handler(q_app):
    def write_to_file(trace, message):
        with open(CRASH_PATH, "w+") as f:
            f.write(message + "\n\n----\n\n" + trace)
            f.close()

    def handle_exception(exc_type, exc_value, exc_traceback):
        """ handle all exceptions """

        ## KeyboardInterrupt is a special case.
        ## We don't raise the error dialog when it occurs.
        if issubclass(exc_type, KeyboardInterrupt):
            q_app.quit()
            return

        filename, line, dummy, dummy = traceback.extract_tb(exc_traceback).pop()
        filename = os.path.basename(filename)
        error = "%s: %s" % (exc_type.__name__, exc_value)

        whole_message = "A critical error has occured.\n\n" \
            + "%s\n\n" % error \
            + "It occurred at line %d of file %s." % (line, filename)

        trace = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        write_to_file(trace, whole_message)

        try:
            msg = QMessageBox()
            msg.critical(
                None,
                "Error",
                whole_message
            )
        except Exception as e:
            print(e)

        relaunch()

    # install handler for exceptions
    sys.excepthook = handle_exception
    sys._excepthook = sys.excepthook

