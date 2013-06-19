__author__ = 'mwolf'

import unittest
from mockito import mock, when, verify, unstub, any as any_value
import livestatus_service
from livestatus_service.livestatus import perform_query, perform_command


class LivestatusTests(unittest.TestCase):

    def tearDown(self):
        unstub()

    def test_should_write_query_to_socket(self):
        mock_configuration = mock()
        mock_socket = mock()
        mock_configuration.livestatus_socket = '/path/to/socket'
        when(livestatus_service.livestatus).get_current_configuration().thenReturn(mock_configuration)
        when(livestatus_service.livestatus.socket).socket(any_value(), any_value()).thenReturn(mock_socket)

        perform_query('test')

        verify(mock_socket).send('test\n')

    def test_should_perform_command_and_receive_ok(self):
        mock_configuration = mock()
        mock_socket = mock()
        mock_configuration.livestatus_socket = '/path/to/socket'
        when(livestatus_service.livestatus).get_current_configuration().thenReturn(mock_configuration)
        when(livestatus_service.livestatus.socket).socket(any_value(), any_value()).thenReturn(mock_socket)

        perform_command(any_value())

        verify(mock_socket).send(any_value())