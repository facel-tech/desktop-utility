import logging


class CustomFormatter(logging.Formatter):
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: "[DEBUG]" + format,
        logging.INFO: "[INFO]" + format,
        logging.WARNING: "[WARNING]" + format,
        logging.ERROR: "[ERROR]" + format,
        logging.CRITICAL: "[CRITICAL]" + format,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
