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
import time

'''
    Wraps the icinga named pipe to expose it to python code. It allows writing
    commands to the file only - queries are not supported.
'''

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
