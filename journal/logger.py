import logging
from logging.handlers import RotatingFileHandler
import config


# This is the default name for the Journal logger
JOURNAL_LOGGER_NAME = "journal"


def configure_logger(
        name = JOURNAL_LOGGER_NAME,
        log_file = config.LOGGING_FILE_NAME,
        level = config.LOGGING_LEVEL,
        size_limit = config.LOGGING_MAX_LOG_SIZE,
        backup_count = config.LOGGING_FILE_BACKUP_COUNT):
    """ Sets up the default Journal logger based on the values from config module """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.hasHandlers():
        handler = RotatingFileHandler(log_file, maxBytes=size_limit, backupCount=backup_count)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)


def journal_logger():
    """
        Shortcut for retrieving default Journal logger. Make sure
        you've initialized the logger with a call of the configure_logger
        function (needs to be done just once at the start of the app).
    """
    return logging.getLogger(JOURNAL_LOGGER_NAME)
