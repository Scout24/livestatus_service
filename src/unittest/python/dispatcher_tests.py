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
