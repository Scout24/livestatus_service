import unittest
from mock import patch, call, PropertyMock
import livestatus_service


class LivestatusServiceInitializationTests(unittest.TestCase):

    @patch('livestatus_service.initialize_logging')
    @patch('livestatus_service.Configuration')
    def test_should_initialize_logging_with_current_configuration(self, mock_config, mock_initialize_logging):
        config_properties = PropertyMock()
        config_properties.log_file = '/foo/bar/baz.log'
        mock_config.return_value = config_properties


        livestatus_service.initialize('/foo/bar/config.cfg')

        self.assertEquals(mock_initialize_logging.call_args, call(config_properties.log_file))
