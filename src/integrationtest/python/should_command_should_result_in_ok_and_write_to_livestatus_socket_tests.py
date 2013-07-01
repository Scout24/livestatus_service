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
                self.assertEquals(result.read(), 'OK\n')
                self.assertTrue('DISABLE_HOST_NOTIFICATIONS;devica01' in livesocket.incoming.get())


if __name__ == '__main__':
    unittest.main()
