import logging
from config import config


LOGGING_LEVEL = getattr(logging, config.get('log_level').upper())


def setup_logging(name):
    logging.basicConfig(format='%(levelname)s:%(message)s', level=LOGGING_LEVEL)
    return logging.getLogger(name)
