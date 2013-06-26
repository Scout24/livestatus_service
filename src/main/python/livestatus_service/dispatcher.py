from __future__ import absolute_import

from livestatus_service.livestatus import perform_query as perform_livestatus_query
from livestatus_service.livestatus import perform_command as perform_livestatus_command
from livestatus_service.configuration import get_current_configuration

from livestatus_service.icinga import perform_command as perform_icinga_command


def perform_query(query, key=None, handler=None):
    configuration = get_current_configuration()
    if handler is None or handler == 'livestatus':
        socket_path = configuration.livestatus_socket
        return perform_livestatus_query(query, socket_path, key)

    raise ValueError('No handler {0}.'.format(handler))


def perform_command(command, key=None, handler=None):
    configuration = get_current_configuration()

    if handler is None or handler == 'livestatus':
        socket_path = configuration.livestatus_socket
        return perform_livestatus_command(command, socket_path, key)
    elif handler == 'icinga':
        command_file_path = configuration.icinga_command_file
        return perform_icinga_command(command, command_file_path, key)

    raise ValueError('No handler {0}.'.format(handler))
