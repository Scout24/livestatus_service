import multiprocessing
import socket
import os
import time


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
        connection, client_address = _socket.accept()
        try:
            while True:
                data = connection.recv(8192)
                queue.put(data)
                if data is None and response:
                    connection.sendall(response.encode('utf-8'))
                else:
                    break
        finally:
            connection.close()


class LiveSocket(object):
    def __init__(self, path, response):
        self.path = path
        self.response = response

    def incoming_writes(self):
        items = []
        while True:
            try:
                items.append(self.incoming.get_nowait())
            except:
                break
        return items


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
        time.sleep(5)

    def stop_listening(self):
        self._process.terminate()
