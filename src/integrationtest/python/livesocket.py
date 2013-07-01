import multiprocessing
import socket
import os
import sys


def _listen_and_respond(path, response, queue):
    _socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        os.unlink(path)
    except OSError:
        if os.path.exists(path):
            raise
    _socket.bind(path)
    _socket.listen(1)

    while True:
        print >>sys.stderr, 'waiting for a connection'
        connection, client_address = _socket.accept()
        try:
            print >>sys.stderr, 'connection from', client_address

            while True:
                data = connection.recv(8192)
                queue.put(data)
                if data is None and response:
                    connection.sendall(response)
                else:
                    break
        finally:
            connection.close()


class LiveSocket(object):
    def __init__(self, path, response):
        self.path = path
        self.response = response


    def __enter__(self):
        self.start_listening()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.stop_listening()

    def start_listening(self):
        worker = _listen_and_respond
        self.incoming = multiprocessing.Queue()
        self._process = multiprocessing.Process(target=worker, args=(self.path, self.response, self.incoming))
        self._process.start()

    def stop_listening(self):
        self._process.terminate()
