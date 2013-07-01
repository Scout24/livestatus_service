'''
    Wraps the livestatus UNIX socket to expose it to python code. Provides abstract
    access to the socket and formatting functions to deal with the livestatus
    responses.
'''

from __future__ import absolute_import
import json
import logging
import socket
import time


LOGGER = logging.getLogger('livestatus.livestatus')


class NoColumnsSpecifiedException(BaseException):
    pass


class LivestatusSocket(object):
    BUFFER_SIZE = 8192

    def __init__(self, socket_path):
        self.socket_path = socket_path
        self.connected = False

    def _connect(self):
        self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._socket.connect(self.socket_path)
        self.connected = True

    def connect_if_necessary(self):
        if not self.connected:
            self._connect()

    def send_command(self, command):
        self.connect_if_necessary()
        timestamp = str(int(time.time()))
        self._socket.send("COMMAND [{0}] {1}\n".format(timestamp, command).encode('utf-8'))
        self._socket.shutdown(socket.SHUT_WR)

    def send_query_and_receive_json_answer(self, query):
        self.connect_if_necessary()
        self._socket.send("{0}\nOutputFormat: json\n".format(query).encode('utf-8'))
        self._socket.shutdown(socket.SHUT_WR)
        return self.receive_json_answer()

    def receive_json_answer(self):
        total_data = []
        while True:
            data = self._socket.recv(self.BUFFER_SIZE)
            if not data:
                break
            total_data.append(data)
        answer = ''.join(total_data)
        answer = json.loads(answer)
        return answer


def perform_query(query, socket_path, key=None):
    livestatus_socket = LivestatusSocket(socket_path)
    answer = livestatus_socket.send_query_and_receive_json_answer(query)
    formatted_answer = format_answer(query, answer, key)

    return json.dumps(formatted_answer, sort_keys=False, indent=4)


def perform_command(command, socket_path, key=None):
    livestatus_socket = LivestatusSocket(socket_path)
    livestatus_socket.send_command(command)
    return "OK"


def format_answer(query, answer, key_to_use):
    """
    Answers come in two different types :
     - Columns were specified in the LQL, so the query must be parsed
     - Columns were not specified, they are then the first line in the result, so the answer must be parsed
    """
    try:
        columns_to_show = determine_columns_to_show_from_query(query)
    except NoColumnsSpecifiedException:
        columns_to_show = determine_columns_to_show_from_answer(answer)
        if len(answer) <= 1:
            message = 'Cannot format answer {0}, either the column definitions or the contents are missing'
            raise ValueError(message.format(answer))
        answer = answer[1:]  # first element is a list with column names, remove it

    if key_to_use is not None and not key_to_use in columns_to_show:
        raise RuntimeError('Cannot use %s as key since it is not a column in the result' % key_to_use)

    if key_to_use is None:
        return _list_of_rows(answer, columns_to_show)
    else:
        return _dictionary_of_rows(answer, columns_to_show, key_to_use)


def determine_columns_to_show_from_query(query):
    for query_line in query.splitlines():
        if 'Columns:' in query_line:
            columns_to_show = query_line.split('Columns:')[1].split()
            return columns_to_show
    raise NoColumnsSpecifiedException()


def determine_columns_to_show_from_answer(answer):
    columns_line = answer[0]
    return columns_line


def _list_of_rows(answer, columns_to_show):
    formatted_answer = []
    for row in answer:
        formatted_row = _map_columns_to_show_with_one_row_of_actual_values(columns_to_show, row)
        formatted_answer.append(formatted_row)
    return formatted_answer


def _dictionary_of_rows(answer, columns_to_show, key_to_use):
    formatted_answer = {}
    for row in answer:
        formatted_row = _map_columns_to_show_with_one_row_of_actual_values(columns_to_show, row)
        if key_to_use not in formatted_row:
            LOGGER.warn('Skipping row {0} because the key {1} is missing'.format(formatted_row, key_to_use))
            continue
        formatted_answer[str(formatted_row[key_to_use])] = formatted_row
    return formatted_answer


def _map_columns_to_show_with_one_row_of_actual_values(columns_to_show, row):
    return dict(zip(columns_to_show, row))
