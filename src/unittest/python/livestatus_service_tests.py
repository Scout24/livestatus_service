import unittest
from mock import patch, call, PropertyMock
import livestatus_service
from livestatus_service import initialize_logging


class LivestatusServiceInitializationTests(unittest.TestCase):

    @patch('livestatus_service.initialize_logging')
    @patch('livestatus_service.Configuration')
    def test_should_initialize_logging_with_current_configuration(self, mock_config, mock_initialize_logging):
        config_properties = PropertyMock()
        config_properties.log_file = '/foo/bar/baz.log'
        mock_config.return_value = config_properties


        livestatus_service.initialize('/foo/bar/config.cfg')

        self.assertEquals(mock_initialize_logging.call_args, call(config_properties.log_file))

    @patch('livestatus_service.logging.FileHandler')
    def test_initialize_logging_should_create_log_file_handler(self, mock_file_handler):
        initialize_logging('/path/to/log/file')

        self.assertEquals(mock_file_handler.call_args, call('/path/to/log/file'))
