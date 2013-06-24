__version__ = "${version}"
'''
    Livestatus-service wraps a MK-livestatus UNIX socket as a Flask application.
    This is the initialization code for the application.
'''

import logging

from .configuration import Configuration


def initialize(config_file):
    current_configuration = Configuration(config_file)
    initialize_logging(current_configuration.log_file)


def initialize_logging(log_file):
    formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")

    log_file_handler = logging.FileHandler(log_file)
    log_file_handler.setLevel(logging.DEBUG)
    log_file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    livestatus_logger = logging.getLogger("livestatus")
    livestatus_logger.setLevel(logging.DEBUG)
    livestatus_logger.addHandler(log_file_handler)
    livestatus_logger.addHandler(console_handler)

    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.setLevel(logging.INFO)
    werkzeug_logger.addHandler(log_file_handler)
    werkzeug_logger.addHandler(console_handler)
