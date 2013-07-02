import unittest
try:
    from urllib2 import urlopen
except:
    from urllib.request import urlopen
from mock import patch, PropertyMock
import json

from liveserver import LiveServer
from livesocket import LiveSocket

expected_api_call_response = {
    u'devica01': {
        u'notifications_enabled': 1,
        u'host_name': 'devica01'
    },
    u'tuvdbs06': {
        u'notifications_enabled': 1,
        u'host_name': 'tuvdbs06'
    },
    u'tuvdbs05': {
        u'notifications_enabled': 1,
        u'host_name': 'tuvdbs05'
    }
}



class Test(unittest.TestCase):
    @patch('livestatus_service.dispatcher.get_current_configuration')
    def test(self, get_config):
        mock_configuration = PropertyMock()
        mock_configuration.livestatus_socket = './livestatus_socket'
        get_config.return_value = mock_configuration
        with LiveServer() as liveserver:
            socket_response = '[["host_name","notifications_enabled"],["devica01", 1], ["tuvdbs05",1], ["tuvdbs06",1]]'
            with LiveSocket('./livestatus_socket', socket_response) as livesocket:
                api_call_result = urlopen('{0}query?q=GET%20hosts&key=host_name'.format(liveserver.url))
                actual_api_response = json.loads(api_call_result.read().decode('utf-8'))
                self.assertDictEqual(expected_api_call_response, actual_api_response)
                written_to_socket = livesocket.incoming.get()
                self.assertTrue('GET hosts' in written_to_socket and 'OutputFormat: json' in written_to_socket)


if __name__ == '__main__':
    unittest.main()
