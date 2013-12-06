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

from mock import patch, Mock
import unittest

import livestatus_service
from livestatus_service.dispatcher import perform_command, perform_query


class DispatcherTests(unittest.TestCase):

    @patch('livestatus_service.dispatcher.get_current_configuration')
    @patch('livestatus_service.dispatcher.perform_livestatus_command')
    def test_perform_command_should_dispatch_to_livestatus_if_handler_is_livestatus(self, cmd, current_config):
        mock_config = Mock()
        mock_config.livestatus_socket = '/path/to/socket'
        current_config.return_value = mock_config

        perform_command('FOO;bar', None, 'livestatus')

        cmd.assert_called_with('FOO;bar', '/path/to/socket', None)

    @patch('livestatus_service.dispatcher.get_current_configuration')
    @patch('livestatus_service.dispatcher.perform_icinga_command')
    def test_perform_command_should_dispatch_to_icinga_if_handler_is_icinga(self, cmd, current_config):
        mock_config = Mock()
        mock_config.icinga_command_file = '/path/to/commandfile.cmd'
        current_config.return_value = mock_config

        perform_command('FOO;bar', None, 'icinga')

        cmd.assert_called_with('FOO;bar', '/path/to/commandfile.cmd', None)

    @patch('livestatus_service.dispatcher.get_current_configuration')
    def test_perform_command_should_raise_exception_when_handler_does_not_exist(self, current_config):
        mock_config = Mock()
        current_config.return_value = mock_config
        self.assertRaises(BaseException, perform_command, 'FOO;bar', None, 'mylittlepony')

    @patch('livestatus_service.dispatcher.get_current_configuration')
    def test_perform_query_should_raise_exception_when_handler_does_not_exist(self, current_config):
        mock_config = Mock()
        current_config.return_value = mock_config
        self.assertRaises(BaseException, perform_query, 'GET HOSTS', None, 'mylittlepony')

    @patch('livestatus_service.dispatcher.get_current_configuration')
    @patch('livestatus_service.dispatcher.perform_livestatus_query')
    def test_perform_query_should_dispatch_to_livestatus_if_handler_is_livestatus(self, query, current_config):
        mock_config = Mock()
        mock_config.livestatus_socket = '/path/to/socket'
        current_config.return_value = mock_config

        perform_query('FOO;bar', None, 'livestatus')

        query.assert_called_with('FOO;bar', '/path/to/socket', None)
