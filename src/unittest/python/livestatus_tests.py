from __future__ import absolute_import
__author__ = 'Marcel Wolf <marcel.wolf@immobilienscout24.de>, Maximilien Riehl <maximilien.riehl@gmail.com>'

import unittest
from mockito import mock, when, verify, unstub, any as any_value
import livestatus_service
from livestatus_service.livestatus import   perform_query, \
                                            perform_command, \
                                            format_answer,\
                                            _dictionary_of_rows,\
                                            NoColumnsSpecifiedException,\
                                            determine_columns_to_show_from_query


class LivestatusTests(unittest.TestCase):

    def tearDown(self):
        unstub()


    def test_should_read_query_answer_fully(self):
        mock_socket = mock()
        when(mock_socket).recv(any_value()).thenReturn('{').thenReturn('}').thenReturn(None)
        when(livestatus_service.livestatus.socket).socket(any_value(), any_value()).thenReturn(mock_socket)
        when(livestatus_service.livestatus).format_answer(any_value(), any_value(), any_value()).thenReturn(None)
        livestatus_service.livestatus.format_answer = lambda _, x, __: x

        self.assertEqual(perform_query('test', '/path/to/socket'), '{}')


    def test_should_write_query_to_socket(self):
        livestatus_service.livestatus.format_answer = lambda _, x, __: x

        mock_socket = mock()
        when(mock_socket).recv(any_value()).thenReturn('{').thenReturn('}').thenReturn(None)
        when(livestatus_service.livestatus.socket).socket(any_value(), any_value()).thenReturn(mock_socket)
        when(livestatus_service.livestatus).format_answer(any_value(), any_value(), any_value()).thenReturn(None)

        perform_query('test', '/path/to/socket')

        verify(mock_socket).send('test\nOutputFormat: json\n')

    def test_should_open_configured_socket(self):
        mock_socket = mock()
        when(mock_socket).recv(any_value()).thenReturn('{').thenReturn('}').thenReturn(None)
        when(livestatus_service.livestatus.socket).socket(any_value(), any_value()).thenReturn(mock_socket)
        when(livestatus_service.livestatus).format_answer(any_value(), any_value(), any_value()).thenReturn(None)

        livestatus_service.livestatus.perform_query('test', '/path/to/socket')

        verify(mock_socket).connect('/path/to/socket')

    def test_should_perform_command_and_receive_ok(self):
        mock_socket = mock()
        when(livestatus_service.livestatus.time).time().thenReturn(123)
        when(livestatus_service.livestatus.socket).socket(any_value(), any_value()).thenReturn(mock_socket)

        perform_command('foobar', '/path/to/socket')

        verify(mock_socket).send('COMMAND [123] foobar\n')

class LivestatusAnswerParsingTests(unittest.TestCase):

    def setUp(self):
        when(livestatus_service.livestatus.LOGGER).warn(any_value()).thenReturn(None)

    def tearDown(self):
        unstub()

    def test_should_parse_query_with_two_columns(self):
        answer = format_answer('''
GET hosts
Columns: host_name notifications_enabled''', [["devica01",1], ["tuvdbs05",1], ["tuvdbs06",1], ["tuvdbs50",1], ["tuvmpc01",1], ["tuvmpc02",1], ["tuvrep01",1]], 'host_name')
        self.assertEqual(answer, {'devica01': {'notifications_enabled': 1, 'host_name': 'devica01'}, 'tuvrep01': {'notifications_enabled': 1, 'host_name': 'tuvrep01'}, 'tuvdbs06': {'notifications_enabled': 1, 'host_name': 'tuvdbs06'}, 'tuvdbs05': {'notifications_enabled': 1, 'host_name': 'tuvdbs05'}, 'tuvdbs50': {'notifications_enabled': 1, 'host_name': 'tuvdbs50'}, 'tuvmpc01': {'notifications_enabled': 1, 'host_name': 'tuvmpc01'}, 'tuvmpc02': {'notifications_enabled': 1, 'host_name': 'tuvmpc02'}})

    def test_should_raise_exception_when_key_is_not_in_queried_columns(self):
        self.assertRaises(RuntimeError, format_answer, 'GET hosts\nColumns: host_name notifications_enabled', [["devica01",1], ["tuvdbs05",1], ["tuvdbs06",1], ["tuvdbs50",1], ["tuvmpc01",1], ["tuvmpc02",1], ["tuvrep01",1]], 'not_a_valid_key')


    def test_should_raise_exception_when_no_columns_were_specified_in_query(self):
        self.assertRaises(NoColumnsSpecifiedException, determine_columns_to_show_from_query, 'foobar')


    def test_should_raise_exception_when_answer_is_missing_values(self):
        self.assertRaises(ValueError, format_answer, 'GET hosts', [['host_name', 'notifications_enabled']], None)


    def test_should_return_list_when_no_key_is_given(self):
        answer = format_answer('GET hosts\nColumns: host_name notifications_enabled''',
                              [["devica01",'1']],
                               None)
        self.assertEqual(answer, [
                                    {
                                        'notifications_enabled': '1',
                                        'host_name': 'devica01'
                                    },
                                ])

    def test_should_parse_columns_from_answer_when_no_columns_were_specified(self):
        answer = format_answer('GET hosts', [['host_name','notifications_enabled'],['devica01', '1'], ['tuvdbs05','1'], ['tuvdbs06','1']], None)
        self.assertEqual(answer, [{'notifications_enabled': '1', 'host_name': 'devica01'}, {'notifications_enabled': '1', 'host_name': 'tuvdbs05'}, {'notifications_enabled': '1', 'host_name': 'tuvdbs06'}])


    def test_should_parse_query_with_several_columns(self):
        answer = format_answer('GET hosts\nColumns: host_name notifications_enabled accept_passive_checks acknowledged acknowledgement_type action_url',
                               [["devica01",1,1,0,0,""], ["tuvdbs05",1,1,0,0,""], ["tuvdbs06",1,1,0,0,""], ["tuvdbs50",1,1,0,0,""], ["tuvmpc01",1,1,0,0,""], ["tuvmpc02",1,1,0,0,""], ["tuvrep01",1,1,0,0,""]],
                               'host_name')
        self.assertEqual(answer, {'devica01': {'acknowledgement_type': 0, 'notifications_enabled': 1, 'acknowledged': 0, 'action_url': '', 'accept_passive_checks': 1, 'host_name': 'devica01'}, 'tuvrep01': {'acknowledgement_type': 0, 'notifications_enabled': 1, 'acknowledged': 0, 'action_url': '', 'accept_passive_checks': 1, 'host_name': 'tuvrep01'}, 'tuvdbs06': {'acknowledgement_type': 0, 'notifications_enabled': 1, 'acknowledged': 0, 'action_url': '', 'accept_passive_checks': 1, 'host_name': 'tuvdbs06'}, 'tuvdbs05': {'acknowledgement_type': 0, 'notifications_enabled': 1, 'acknowledged': 0, 'action_url': '', 'accept_passive_checks': 1, 'host_name': 'tuvdbs05'}, 'tuvdbs50': {'acknowledgement_type': 0, 'notifications_enabled': 1, 'acknowledged': 0, 'action_url': '', 'accept_passive_checks': 1, 'host_name': 'tuvdbs50'}, 'tuvmpc01': {'acknowledgement_type': 0, 'notifications_enabled': 1, 'acknowledged': 0, 'action_url': '', 'accept_passive_checks': 1, 'host_name': 'tuvmpc01'}, 'tuvmpc02': {'acknowledgement_type': 0, 'notifications_enabled': 1, 'acknowledged': 0, 'action_url': '', 'accept_passive_checks': 1, 'host_name': 'tuvmpc02'}})

    def test_should_parse_two_columns(self):
        answer = format_answer('GET hosts\nColumns: host_name notifications_enabled\nFilter: host_name = devica01\n', [["devica01",1]], None)
        self.assertEqual(answer, [{'notifications_enabled': 1, 'host_name': 'devica01'}])

    def test_should_skip_rows_where_the_key_is_missing(self):
        answer = format_answer('GET hosts\nColumns: foo bar baz\n', [["foo1","bar1", "baz1"], ["foo2", "bar2"]], 'baz')
        self.assertEqual(answer, {'baz1': {'baz': 'baz1', 'foo': 'foo1', 'bar': 'bar1'}})
