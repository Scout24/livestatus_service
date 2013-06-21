import socket
import time
from livestatus_service.configuration import get_current_configuration


BUFFER_SIZE = 8192


class NoColumnsSpecifiedException(BaseException):
    pass


def perform_query(query):
    key_to_use = None
    socket_path = get_current_configuration().livestatus_socket

    livestatus_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    livestatus_socket.connect(socket_path)

    livestatus_socket.send("{0}\n".format(query))
    livestatus_socket.shutdown(socket.SHUT_WR)
    total_data = []
    while True:
        data = livestatus_socket.recv(BUFFER_SIZE)
        if not data:
            break
        total_data.append(data)
    answer = ''.join(total_data)

    return format_answer(query, answer, key_to_use)


def perform_command(command):
    socket_path = get_current_configuration().livestatus_socket

    livestatus_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    livestatus_socket.connect(socket_path)
    timestamp = str(int(time.time()))
    livestatus_socket.send("COMMAND [{0}] {1}\n".format(timestamp, command))
    livestatus_socket.shutdown(socket.SHUT_WR)
    return "OK"


def format_answer(query, answer, key_to_use):
    try:
        columns_to_show = determine_columns_to_show(query)
    except NoColumnsSpecifiedException:
        return answer

    if key_to_use is not None and not key_to_use in columns_to_show:
        raise RuntimeError('Cannot use %s as key since it is not a column in the result' % key_to_use)

    if key_to_use is None:
        return _list_of_rows(answer, columns_to_show)
    else:
        return _dictionary_of_rows(answer, columns_to_show, key_to_use)


def determine_columns_to_show(query):
    for query_line in query.splitlines():
        if 'Columns:' in query_line:
            columns_to_show = query_line.split('Columns:')[1].split()
            return columns_to_show
    raise NoColumnsSpecifiedException()


def _list_of_rows(answer, columns_to_show):
    formatted_answer = []

    for row in answer.split():
        formatted_row = dict(zip(columns_to_show, row.split(';')))
        formatted_answer.append(formatted_row)
    return formatted_answer


def _dictionary_of_rows(answer, columns_to_show, key_to_use):
    formatted_answer = {}

    for row in answer.split():
        formatted_row = dict(zip(columns_to_show, row.split(';')))
        formatted_answer[formatted_row[key_to_use]] = formatted_row
    return formatted_answer
