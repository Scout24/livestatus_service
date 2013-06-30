from mockito import mock, when, verify, unstub, any as any_value
import unittest

import livestatus_service
from livestatus_service.dispatcher import perform_command, perform_query


class DispatcherTests(unittest.TestCase):

    def tearDown(self):
        unstub()

    def test_perform_command_should_dispatch_to_livestatus_if_handler_is_livestatus(self):
        when(livestatus_service.dispatcher).perform_livestatus_command(any_value(), any_value(), any_value()).thenReturn(None)
        mock_config = mock()
        mock_config.livestatus_socket = '/path/to/socket'
        when(livestatus_service.dispatcher).get_current_configuration().thenReturn(mock_config)

        perform_command('FOO;bar', None, 'livestatus')

        verify(livestatus_service.dispatcher).perform_livestatus_command('FOO;bar', '/path/to/socket', None)

    def test_perform_command_should_dispatch_to_icinga_if_handler_is_icinga(self):
        when(livestatus_service.dispatcher).perform_icinga_command(any_value(), any_value(), any_value()).thenReturn(None)
        mock_config = mock()
        mock_config.icinga_command_file = '/path/to/commandfile.cmd'
        when(livestatus_service.dispatcher).get_current_configuration().thenReturn(mock_config)

        perform_command('FOO;bar', None, 'icinga')

        verify(livestatus_service.dispatcher).perform_icinga_command('FOO;bar', '/path/to/commandfile.cmd', None)

    def test_perform_command_should_raise_exception_when_handler_does_not_exist(self):
        mock_config = mock()
        when(livestatus_service.dispatcher).get_current_configuration().thenReturn(mock_config)
        self.assertRaises(BaseException, perform_command, 'FOO;bar', None, 'mylittlepony')

    def test_perform_query_should_raise_exception_when_handler_does_not_exist(self):
        mock_config = mock()
        when(livestatus_service.dispatcher).get_current_configuration().thenReturn(mock_config)
        self.assertRaises(BaseException, perform_query, 'GET HOSTS', None, 'mylittlepony')

    def test_perform_query_should_dispatch_to_livestatus_if_handler_is_livestatus(self):
        when(livestatus_service.dispatcher).perform_livestatus_query(any_value(), any_value(), any_value()).thenReturn(None)
        mock_config = mock()
        mock_config.livestatus_socket = '/path/to/socket'
        when(livestatus_service.dispatcher).get_current_configuration().thenReturn(mock_config)

        perform_query('FOO;bar', None, 'livestatus')

        verify(livestatus_service.dispatcher).perform_livestatus_query('FOO;bar', '/path/to/socket', None)
