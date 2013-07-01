import unittest
try:
    from urllib2 import urlopen
except:
    from urllib.request import urlopen
from mock import patch, PropertyMock

from liveserver import LiveServer
from livesocket import LiveSocket

expected_response = \
'''[\n    {\n        "notifications_enabled": 1, \n        "host_name": "devica01"\n    }, \n    {\n        "notifications_enabled": 1, \n        "host_name": "tuvdbs05"\n    }, \n    {\n        "notifications_enabled": 1, \n        "host_name": "tuvdbs06"\n    }\n]\n'''


class Test(unittest.TestCase):
    @patch('livestatus_service.dispatcher.get_current_configuration')
    def test(self, get_config):
        mock_configuration = PropertyMock()
        mock_configuration.livestatus_socket = './livestatus_socket'
        get_config.return_value = mock_configuration
        with LiveServer() as liveserver:
            response = '[["host_name","notifications_enabled"],["devica01", 1], ["tuvdbs05",1], ["tuvdbs06",1]]'
            with LiveSocket('./livestatus_socket', response) as livesocket:
                result = urlopen('{0}query?q=GET%20hosts'.format(liveserver.url))
                self.assertEquals(result.read(), expected_response)
                written_to_socket = livesocket.incoming.get()
                self.assertTrue('GET hosts' in written_to_socket and 'OutputFormat: json' in written_to_socket)


if __name__ == '__main__':
    unittest.main()
