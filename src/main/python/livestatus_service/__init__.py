'''
The MIT License (MIT)

Copyright (c) 2013 ImmobilienScout24

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

from __future__ import absolute_import
import logging

from .configuration import Configuration

'''
    Livestatus-service wraps a MK-livestatus UNIX socket as a Flask application.
    This is the initialization code for the application.
'''

__version__ = "${version}"


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
