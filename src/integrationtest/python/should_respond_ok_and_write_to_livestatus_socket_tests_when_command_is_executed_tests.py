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

from __future__ import print_function
import unittest
try:
    from urllib2 import urlopen
except:
    from urllib.request import urlopen
from mock import patch, PropertyMock

from liveserver import LiveServer
from livesocket import LiveSocket


class Test(unittest.TestCase):
    @patch('livestatus_service.dispatcher.get_current_configuration')
    def test(self, get_config):
        mock_configuration = PropertyMock()
        mock_configuration.livestatus_socket = './livestatus_socket'
        get_config.return_value = mock_configuration
        with LiveServer() as liveserver:
            with LiveSocket('./livestatus_socket', '{}') as livesocket:
                result = urlopen('{0}cmd?q=DISABLE_HOST_NOTIFICATIONS;devica01'.format(liveserver.url))
                self.assertEquals(result.read(), b'OK\n')
                written_to_socket = livesocket.incoming.get()
                self.assertTrue('DISABLE_HOST_NOTIFICATIONS;devica01' in written_to_socket)


if __name__ == '__main__':
    unittest.main()
