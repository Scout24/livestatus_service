from __future__ import absolute_import

import time
import logging

'''
This file provides function wraps the icinga named pipe to expose it to
python code. It allows writing commands to the file.
'''


LOGGER = logging.getLogger('livestatus.icinga')


def perform_command(command, command_file_path, key=None):
    with open(command_file_path, 'w') as command_file:
        timestamp = str(int(time.time()))
        command_file.write('[{0}] {1}\n'.format(timestamp, command))
    return 'OK'
