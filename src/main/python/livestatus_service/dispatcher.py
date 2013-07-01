'''
    Decides how queries and commands are performed based on the 'handler'.
    Then performs the query or command after determining run-time configuration.
'''

from __future__ import absolute_import
from livestatus_service.configuration import get_current_configuration
from livestatus_service.icinga import perform_command as perform_icinga_command
from livestatus_service.livestatus import perform_query as perform_livestatus_query
from livestatus_service.livestatus import perform_command as perform_livestatus_command


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
