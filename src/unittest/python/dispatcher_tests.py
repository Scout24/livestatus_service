import unittest
from mockito import mock, when, verify, unstub, any as any_value

import livestatus_service
from livestatus_service.dispatcher import perform_command

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
        perform_command('FOO;bar', None, 'mylittlepony')
