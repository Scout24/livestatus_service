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
            data = connection.recv(8192)
            queue.put(data.decode('utf-8'))
            if response:
                connection.sendall(str(response).encode('utf-8'))
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
        time.sleep(5)

    def stop_listening(self):
        self._process.terminate()
