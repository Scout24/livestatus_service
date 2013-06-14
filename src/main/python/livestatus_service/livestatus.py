import socket
import time


def configure_livestatus(configuration):
    global socket_path
    socket_path = configuration.livestatus_socket

def perform_query(query):
    global socket_path

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(socket_path)

    s.send("{0}\n".format(query))
    s.shutdown(socket.SHUT_WR)
    answer = s.recv(100000000)

    return answer

def perform_command(command):
    global socket_path

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(socket_path)
    timestamp = str(int(time.time()))
    s.send("COMMAND [{0}] {1}\n".format(timestamp, command))
    s.shutdown(socket.SHUT_WR)
    return "OK"
