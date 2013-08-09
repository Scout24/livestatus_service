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
import livestatus_service.webapp
import time
try:
    from urllib2 import urlopen
except:
    from urllib.request import urlopen

CONFIGURATION_FILE = "src/integrationtest/resources/livestatus_service_integrationtest.cfg"
MAX_WAITING_SECONDS = 10
TIMEOUT_SECONDS = 0.05


class LiveServer(object):
    def __init__(self):
        self.configuration = livestatus_service.configuration.Configuration(CONFIGURATION_FILE)

        livestatus_service.initialize_logging(self.configuration.log_file)

        self.application = livestatus_service.webapp.application
        self.host = "127.0.0.1"
        self.port = 5000
        self.protocol = "http"

        self.url = "%s://%s:%s/" % (self.protocol, self.host, self.port)

    def __enter__(self):
        self.start_server_process()
        _wait_for(self.is_server_reachable)
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.stop_server_process()

    def is_server_reachable(self):
        try:
            urlopen(self.url, timeout=TIMEOUT_SECONDS).close()
            return True
        except:
            return False

    def start_server_process(self):
        worker = lambda app, port: app.run(port=port)
        self._process = multiprocessing.Process(target=worker, args=(self.application, self.port))
        self._process.start()

    def stop_server_process(self):
        self._process.terminate()


def _wait_for(expression_to_be_true, max_waiting_seconds=MAX_WAITING_SECONDS, interval_seconds=TIMEOUT_SECONDS):
    waited_seconds = 0
    succeeded = False
    while (not succeeded) and (waited_seconds < max_waiting_seconds):
        succeeded = expression_to_be_true()
        time.sleep(interval_seconds)
        waited_seconds += interval_seconds

    return succeeded
