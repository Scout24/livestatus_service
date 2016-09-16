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

from __future__ import absolute_import
from mock import patch
import unittest

import livestatus_service
from livestatus_service.livestatus import (perform_query,
                                           LivestatusSocket,
                                           perform_command,
                                           format_answer,
                                           NoColumnsSpecifiedException,
                                           determine_columns_to_show_from_query)


class LivestatusTests(unittest.TestCase):

    def setUp(self):
        self.path_patcher = patch(
            'livestatus_service.livestatus.os.path.exists')
        self.path = self.path_patcher.start()
        self.path.return_value = True

    def tearDown(self):
        self.path_patcher.stop()

    def test_should_crash_with_appropriate_error_message_when_socket_not_available(self):
        self.path.return_value = False

        try:
            LivestatusSocket('this-path-does-not-exist')
        except RuntimeError as expected_exception:
            self.assertEqual(
                str(expected_exception), ('Could not connect to livestatus socket ' +
                                          'at this-path-does-not-exist, perhaps ' +
                                          'icinga is not running or mk-livestatus ' +
                                          'is not installed?'))
        else:
            self.fail(
                'Socket instantiation with wrong path should throw an error')

    @patch('livestatus_service.livestatus.format_answer')
    @patch('livestatus_service.livestatus.socket.socket')
    def test_should_read_query_answer_fully(self, mock_socket, format_answer):
        mock_socket.return_value.recv.side_effect = [b'{}', None]
        format_answer.side_effect = lambda _, x, __: x

        self.assertEqual(perform_query('test', '/path/to/socket'), '{}')

    @patch('livestatus_service.livestatus.format_answer')
    @patch('livestatus_service.livestatus.socket.socket')
    def test_should_write_query_to_socket(self, mock_socket, format_answer):
        mock_socket.return_value.recv.side_effect = [b'{}', None]
        format_answer.side_effect = lambda _, x, __: x

        perform_query('test', '/path/to/socket')

        mock_socket.return_value.send.assert_called_with(
            b'test\nOutputFormat: json\n')

    @patch('livestatus_service.livestatus.format_answer')
    @patch('livestatus_service.livestatus.socket.socket')
    def test_should_open_configured_socket(self, mock_socket, format_answer):
        mock_socket.return_value.recv.side_effect = [b'{}', None]
        format_answer.side_effect = lambda _, x, __: x

        livestatus_service.livestatus.perform_query('test', '/path/to/socket')

        mock_socket.return_value.connect.assert_called_with('/path/to/socket')

    @patch('livestatus_service.livestatus.time.time')
    @patch('livestatus_service.livestatus.socket.socket')
    def test_should_perform_command_and_receive_ok(self, mock_socket, time):
        time.return_value = 123

        perform_command('foobar', '/path/to/socket')

        mock_socket.return_value.send.assert_called_with(
            b'COMMAND [123] foobar\n')


class LivestatusAnswerParsingTests(unittest.TestCase):

    def setUp(self):
        self.logger_patcher = patch(
            'livestatus_service.livestatus.LOGGER.warn')
        self.logger_patcher.start()

    def tearDown(self):
        self.logger_patcher.stop()

    def test_should_parse_query_with_two_columns(self):
        answer = format_answer('''
GET hosts
Columns: host_name notifications_enabled''', [["devica01", 1], ["tuvdbs05", 1], ["tuvdbs06", 1], ["tuvdbs50", 1], ["tuvmpc01", 1], ["tuvmpc02", 1], ["tuvrep01", 1]], 'host_name')
        self.assertEqual(answer, {
            'devica01': {
                'notifications_enabled': 1,
                'host_name': 'devica01'
            },
            'tuvrep01': {
                'notifications_enabled': 1,
                'host_name': 'tuvrep01'
            },
            'tuvdbs06': {
                'notifications_enabled': 1,
                'host_name': 'tuvdbs06'
            },
            'tuvdbs05': {
                'notifications_enabled': 1,
                'host_name': 'tuvdbs05'
            },
            'tuvdbs50': {
                'notifications_enabled': 1,
                'host_name': 'tuvdbs50'
            },
            'tuvmpc01': {
                'notifications_enabled': 1,
                'host_name': 'tuvmpc01'
            },
            'tuvmpc02': {
                'notifications_enabled': 1,
                'host_name': 'tuvmpc02'
            }})

    def test_should_raise_exception_when_key_is_not_in_queried_columns(self):
        self.assertRaises(RuntimeError, format_answer, 'GET hosts\nColumns: host_name notifications_enabled', [
                          ["devica01", 1], ["tuvdbs05", 1], ["tuvdbs06", 1], ["tuvdbs50", 1], ["tuvmpc01", 1], ["tuvmpc02", 1], ["tuvrep01", 1]], 'not_a_valid_key')

    def test_should_raise_exception_when_no_columns_were_specified_in_query(self):
        self.assertRaises(NoColumnsSpecifiedException,
                          determine_columns_to_show_from_query, 'foobar')

    def test_should_determine_columns_from_stats_query(self):
        self.assertEquals(["avg perf_data"],
                          determine_columns_to_show_from_query("GET services\nFilter: description ~ CPU\nFilter: host_name ~ somehost\nStats: avg perf_data"))

    def test_should_raise_exception_when_answer_is_missing_values(self):
        self.assertRaises(ValueError,
                          format_answer, 'GET hosts', [['host_name', 'notifications_enabled']], None)

    def test_should_return_list_when_no_key_is_given(self):
        answer = format_answer(
            'GET hosts\nColumns: host_name notifications_enabled''',
            [["devica01", '1']],
            None)
        self.assertEqual(answer, [
            {
                'notifications_enabled': '1',
                'host_name': 'devica01'
            },
        ])

    def test_should_parse_columns_from_answer_when_no_columns_were_specified(self):
        answer = format_answer(
            'GET hosts', [['host_name', 'notifications_enabled'], ['devica01', '1'], ['tuvdbs05', '1'], ['tuvdbs06', '1']], None)
        self.assertEqual(answer, [{'notifications_enabled': '1', 'host_name': 'devica01'}, {
                         'notifications_enabled': '1', 'host_name': 'tuvdbs05'}, {'notifications_enabled': '1', 'host_name': 'tuvdbs06'}])

    def test_should_parse_query_with_several_columns(self):
        answer = format_answer(
            'GET hosts\nColumns: host_name notifications_enabled accept_passive_checks acknowledged acknowledgement_type action_url',
            [["devica01", 1, 1, 0, 0, ""], ["tuvdbs05", 1, 1, 0, 0, ""], ["tuvdbs06", 1, 1, 0, 0, ""], [
             "tuvdbs50", 1, 1, 0, 0, ""], ["tuvmpc01", 1, 1, 0, 0, ""], ["tuvmpc02", 1, 1, 0, 0, ""], ["tuvrep01", 1, 1, 0, 0, ""]],
            'host_name')
        self.assertEqual(
            answer, {
                'devica01': {
                    'acknowledgement_type': 0,
                    'notifications_enabled': 1,
                    'acknowledged': 0,
                    'action_url': '',
                    'accept_passive_checks': 1,
                    'host_name': 'devica01'
                },
                'tuvrep01': {
                    'acknowledgement_type': 0,
                    'notifications_enabled': 1,
                    'acknowledged': 0,
                    'action_url': '',
                    'accept_passive_checks': 1,
                    'host_name': 'tuvrep01'
                },
                'tuvdbs06': {
                    'acknowledgement_type': 0,
                    'notifications_enabled': 1,
                    'acknowledged': 0,
                    'action_url': '',
                    'accept_passive_checks': 1,
                    'host_name': 'tuvdbs06'
                },
                'tuvdbs05': {
                    'acknowledgement_type': 0,
                    'notifications_enabled': 1,
                    'acknowledged': 0,
                    'action_url': '',
                    'accept_passive_checks': 1,
                    'host_name': 'tuvdbs05'
                },
                'tuvdbs50': {
                    'acknowledgement_type': 0,
                    'notifications_enabled': 1,
                    'acknowledged': 0,
                    'action_url': '',
                    'accept_passive_checks': 1,
                    'host_name': 'tuvdbs50'
                },
                'tuvmpc01': {
                    'acknowledgement_type': 0,
                    'notifications_enabled': 1,
                    'acknowledged': 0,
                    'action_url': '',
                    'accept_passive_checks': 1,
                    'host_name': 'tuvmpc01'
                },
                'tuvmpc02': {
                    'acknowledgement_type': 0,
                    'notifications_enabled': 1,
                    'acknowledged': 0,
                    'action_url': '',
                    'accept_passive_checks': 1,
                    'host_name': 'tuvmpc02'
                }})

    def test_should_parse_two_columns(self):
        answer = format_answer(
            'GET hosts\nColumns: host_name notifications_enabled\nFilter: host_name = devica01\n', [["devica01", 1]], None)
        self.assertEqual(
            answer, [{'notifications_enabled': 1, 'host_name': 'devica01'}])

    def test_should_skip_rows_where_the_key_is_missing(self):
        answer = format_answer('GET hosts\nColumns: foo bar baz\n', [
                               ["foo1", "bar1", "baz1"], ["foo2", "bar2"]], 'baz')
        self.assertEqual(
            answer, {'baz1': {'baz': 'baz1', 'foo': 'foo1', 'bar': 'bar1'}})
