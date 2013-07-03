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
from livestatus_service.configuration import get_current_configuration
from livestatus_service.icinga import perform_command as perform_icinga_command
from livestatus_service.livestatus import perform_query as perform_livestatus_query
from livestatus_service.livestatus import perform_command as perform_livestatus_command

'''
    Decides how queries and commands are performed based on the 'handler'.
    Then performs the query or command after determining run-time configuration.
'''


def perform_query(query, key=None, handler=None):
    configuration = get_current_configuration()
    if _is_livestatus_handler(handler):
        socket_path = configuration.livestatus_socket
        return perform_livestatus_query(query, socket_path, key)

    raise ValueError('No handler {0}.'.format(handler))


def perform_command(command, key=None, handler=None):
    configuration = get_current_configuration()

    if _is_livestatus_handler(handler):
        socket_path = configuration.livestatus_socket
        return perform_livestatus_command(command, socket_path, key)
    elif handler == 'icinga':
        command_file_path = configuration.icinga_command_file
        return perform_icinga_command(command, command_file_path, key)

    raise ValueError('No handler {0}.'.format(handler))


def _is_livestatus_handler(handler):
    return handler is None or handler == 'livestatus'
