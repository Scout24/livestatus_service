'''
    Wraps the icinga named pipe to expose it to python code. It allows writing
    commands to the file only - queries are not supported.
'''

from __future__ import absolute_import
import logging
import time


LOGGER = logging.getLogger('livestatus.icinga')


def perform_command(command, command_file_path, key=None):
    icinga_command_file = IcingaCommandFile(command_file_path)
    icinga_command_file.send_command(command)
    return 'OK'


class IcingaCommandFile(object):

    def __init__(self, command_file_path):
        self.command_file_path = command_file_path

    def send_command(self, command):
        with open(self.command_file_path, 'w') as command_file:
            timestamp = str(int(time.time()))
            command_file.write('[{0}] {1}\n'.format(timestamp, command).encode('utf-8'))
