import socket
import time
from livestatus_service.configuration import get_current_configuration


BUFFER_SIZE = 8192


def perform_query(query):
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

    return answer


def perform_command(command):
    socket_path = get_current_configuration().livestatus_socket

    livestatus_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    livestatus_socket.connect(socket_path)
    timestamp = str(int(time.time()))
    livestatus_socket.send("COMMAND [{0}] {1}\n".format(timestamp, command))
    livestatus_socket.shutdown(socket.SHUT_WR)
    return "OK"
