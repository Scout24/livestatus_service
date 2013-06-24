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


    def test_should_write_query_to_socket(self):
        mock_configuration = mock()
        mock_socket = mock()
        mock_configuration.livestatus_socket = '/path/to/socket'
        when(livestatus_service.livestatus).get_current_configuration().thenReturn(mock_configuration)
        when(livestatus_service.livestatus.socket).socket(any_value(), any_value()).thenReturn(mock_socket)
        when(livestatus_service.livestatus).format_answer(any_value(), any_value(), any_value()).thenReturn(None)

        perform_query('test')

        verify(mock_socket).send('test\n')

    def test_should_open_configured_socket(self):
        mock_configuration = mock()
        mock_socket = mock()
        mock_configuration.livestatus_socket = '/path/to/socket'
        when(livestatus_service.livestatus).get_current_configuration().thenReturn(mock_configuration)
        when(livestatus_service.livestatus.socket).socket(any_value(), any_value()).thenReturn(mock_socket)
        when(livestatus_service.livestatus).format_answer(any_value(), any_value(), any_value()).thenReturn(None)

        livestatus_service.livestatus.perform_query('test')

        verify(mock_socket).connect('/path/to/socket')

    def test_should_perform_command_and_receive_ok(self):
        mock_configuration = mock()
        mock_socket = mock()
        mock_configuration.livestatus_socket = '/path/to/socket'
        when(livestatus_service.livestatus.time).time().thenReturn(123)
        when(livestatus_service.livestatus).get_current_configuration().thenReturn(mock_configuration)
        when(livestatus_service.livestatus.socket).socket(any_value(), any_value()).thenReturn(mock_socket)

        perform_command('foobar')

        verify(mock_socket).send('COMMAND [123] foobar\n')

class LivestatusAnswerParsingTests(unittest.TestCase):

    def test_should_parse_query_with_two_columns(self):
        answer = format_answer('''
GET hosts
Columns: host_name notifications_enabled''', 'devica01;1 tuvdbs05;1 tuvdbs06;1', 'host_name')
        self.assertEqual(answer, {
                                    'devica01': {
                                        'notifications_enabled': '1',
                                        'host_name': 'devica01'
                                    },
                                    'tuvdbs05': {
                                        'notifications_enabled': '1',
                                        'host_name': 'tuvdbs05'
                                    },
                                    'tuvdbs06': {
                                        'notifications_enabled': '1',
                                        'host_name': 'tuvdbs06'
                                    }
                        })

    def test_should_raise_exception_when_key_is_not_in_queried_columns(self):
        self.assertRaises(RuntimeError, format_answer, 'GET hosts\nColumns: host_name notifications_enabled', 'devica01;1 tuvdbs05;1 tuvdbs06;1', 'not_a_valid_key')


    def test_should_raise_exception_when_no_columns_were_specified_in_query(self):
        self.assertRaises(NoColumnsSpecifiedException, determine_columns_to_show_from_query, 'foo;1 bar;2')


    def test_should_raise_exception_when_answer_is_missing_values(self):
        self.assertRaises(ValueError, format_answer, 'GET hosts', 'host_name;notifications_enabled', None)


    def test_should_return_list_when_no_key_is_given(self):
        answer = format_answer('GET hosts\nColumns: host_name notifications_enabled''',
                               'devica01;1 tuvdbs05;1 tuvdbs06;1',
                               None)
        self.assertEqual(answer, [
                                    {
                                        'notifications_enabled': '1',
                                        'host_name': 'devica01'
                                    },
                                    {
                                        'notifications_enabled': '1',
                                        'host_name': 'tuvdbs05'
                                    },
                                    {
                                        'notifications_enabled': '1',
                                        'host_name': 'tuvdbs06'
                                    }
                                ])

    def test_should_parse_columns_from_answer_when_no_columns_were_specified(self):
        answer = format_answer('GET hosts', 'host_name;notifications_enabled\ndevica01;1 tuvdbs05;1 tuvdbs06;1', None)
        self.assertEqual(answer, [{'notifications_enabled': '1', 'host_name': 'devica01'}, {'notifications_enabled': '1', 'host_name': 'tuvdbs05'}, {'notifications_enabled': '1', 'host_name': 'tuvdbs06'}])


    def test_should_skip_row_when_key_is_missing_from_row(self):
        result = _dictionary_of_rows(
                        'foo1;bar1;baz1\nfoo2;bar2',
                        ['foo_column', 'bar_column', 'baz_column'],
                        'baz_column')

        self.assertEquals(result,  {'baz1': {
                                        'baz_column': 'baz1',
                                        'bar_column': 'bar1',
                                        'foo_column': 'foo1'}
                                    })

    def test_should_parse_query_with_several_columns(self):
        answer = format_answer('GET hosts\nColumns: host_name notifications_enabled accept_passive_checks acknowledged acknowledgement_type action_url',
                               'devica01;1;1;0;0; tuvdbs05;1;1;0;0; tuvdbs06;1;1;0;0; tuvdbs50;1;1;0;0; tuvmpc01;1;1;0;0; tuvmpc02;1;1;0;0; tuvrep01;1;1;0;0;',
                               'host_name')

        self.assertEqual(answer, {
                                    'devica01': {
                                        'acknowledgement_type': '0',
                                        'notifications_enabled': '1',
                                        'acknowledged': '0',
                                        'action_url': '',
                                        'accept_passive_checks': '1',
                                        'host_name': 'devica01'
                                    },
                                    'tuvrep01': {
                                        'acknowledgement_type': '0',
                                        'notifications_enabled': '1',
                                        'acknowledged': '0',
                                        'action_url': '',
                                        'accept_passive_checks': '1',
                                        'host_name': 'tuvrep01'
                                    },
                                    'tuvdbs06': {
                                        'acknowledgement_type': '0',
                                        'notifications_enabled': '1',
                                        'acknowledged': '0',
                                        'action_url': '',
                                        'accept_passive_checks': '1',
                                        'host_name': 'tuvdbs06'
                                    },
                                    'tuvdbs05': {
                                        'acknowledgement_type': '0',
                                        'notifications_enabled': '1',
                                        'acknowledged': '0',
                                        'action_url': '',
                                        'accept_passive_checks': '1',
                                        'host_name': 'tuvdbs05'
                                    },
                                    'tuvdbs50': {
                                        'acknowledgement_type': '0',
                                        'notifications_enabled': '1',
                                        'acknowledged': '0',
                                        'action_url': '',
                                        'accept_passive_checks': '1',
                                        'host_name': 'tuvdbs50'
                                    },
                                    'tuvmpc01': {
                                        'acknowledgement_type': '0',
                                        'notifications_enabled': '1',
                                        'acknowledged': '0',
                                        'action_url': '',
                                        'accept_passive_checks': '1',
                                        'host_name': 'tuvmpc01'
                                    },
                                    'tuvmpc02': {
                                        'acknowledgement_type': '0',
                                        'notifications_enabled': '1',
                                        'acknowledged': '0',
                                        'action_url': '',
                                        'accept_passive_checks': '1',
                                        'host_name': 'tuvmpc02'
                                    }
                                })


    def test_should_parse_query_with_several_columns_when_no_columns_are_specified(self):
        answer = format_answer('GET hosts',
                               'host_name;notifications_enabled;accept_passive_checks;acknowledged;acknowledgement_type;action_url\ndevica01;1;1;0;0; tuvdbs05;1;1;0;0; tuvdbs06;1;1;0;0; tuvdbs50;1;1;0;0; tuvmpc01;1;1;0;0; tuvmpc02;1;1;0;0; tuvrep01;1;1;0;0;',
                               'host_name')

        self.assertEqual(answer, {
                                    'devica01': {
                                        'acknowledgement_type': '0',
                                        'notifications_enabled': '1',
                                        'acknowledged': '0',
                                        'action_url': '',
                                        'accept_passive_checks': '1',
                                        'host_name': 'devica01'
                                    },
                                    'tuvrep01': {
                                        'acknowledgement_type': '0',
                                        'notifications_enabled': '1',
                                        'acknowledged': '0',
                                        'action_url': '',
                                        'accept_passive_checks': '1',
                                        'host_name': 'tuvrep01'
                                    },
                                    'tuvdbs06': {
                                        'acknowledgement_type': '0',
                                        'notifications_enabled': '1',
                                        'acknowledged': '0',
                                        'action_url': '',
                                        'accept_passive_checks': '1',
                                        'host_name': 'tuvdbs06'
                                    },
                                    'tuvdbs05': {
                                        'acknowledgement_type': '0',
                                        'notifications_enabled': '1',
                                        'acknowledged': '0',
                                        'action_url': '',
                                        'accept_passive_checks': '1',
                                        'host_name': 'tuvdbs05'
                                    },
                                    'tuvdbs50': {
                                        'acknowledgement_type': '0',
                                        'notifications_enabled': '1',
                                        'acknowledged': '0',
                                        'action_url': '',
                                        'accept_passive_checks': '1',
                                        'host_name': 'tuvdbs50'
                                    },
                                    'tuvmpc01': {
                                        'acknowledgement_type': '0',
                                        'notifications_enabled': '1',
                                        'acknowledged': '0',
                                        'action_url': '',
                                        'accept_passive_checks': '1',
                                        'host_name': 'tuvmpc01'
                                    },
                                    'tuvmpc02': {
                                        'acknowledgement_type': '0',
                                        'notifications_enabled': '1',
                                        'acknowledged': '0',
                                        'action_url': '',
                                        'accept_passive_checks': '1',
                                        'host_name': 'tuvmpc02'
                                    }
                                })


    def test_should_parse_mk_example_together_with_one_key(self):
        mk_example_lines = ["acknowledged;action_url;address;alias;check_command;check_period;checks_enabled;contacts;in_check_period;in_notification_period;is_flapping;last_check;last_state_change;name;notes;notes_url;notification_period;scheduled_downtime_depth;state;total_services", "0;/nagios/pnp/index.php?host=$HOSTNAME$;127.0.0.1;Acht;check-mk-ping;;1;check_mk,hh;1;1;0;1256194120;1255301430;Acht;;;24X7;0;0;7", "0;/nagios/pnp/index.php?host=$HOSTNAME$;127.0.0.1;DREI;check-mk-ping;;1;check_mk,hh;1;1;0;1256194120;1255301431;DREI;;;24X7;0;0;1", "0;/nagios/pnp/index.php?host=$HOSTNAME$;127.0.0.1;Drei;check-mk-ping;;1;check_mk,hh;1;1;0;1256194120;1255301435;Drei;;;24X7;0;0;4"]

        answer = format_answer('GET hosts',
                                '\n'.join(mk_example_lines),
                               'alias')
        self.assertEqual(answer, {
                                    'Acht': {
                                        'check_period': '',
                                        'state': '0',
                                        'checks_enabled': '1',
                                        'name': 'Acht',
                                        'contacts': 'check_mk,hh',
                                        'notification_period': '24X7',
                                        'last_state_change': '1255301430',
                                        'notes': '',
                                        'check_command': 'check-mk-ping',
                                        'acknowledged': '0',
                                        'in_notification_period': '1',
                                        'last_check': '1256194120',
                                        'alias': 'Acht',
                                        'action_url': '/nagios/pnp/index.php?host=$HOSTNAME$',
                                        'in_check_period': '1',
                                        'notes_url': '',
                                        'address': '127.0.0.1',
                                        'is_flapping': '0',
                                        'scheduled_downtime_depth': '0',
                                        'total_services': '7'
                                    },
                                    'DREI': {
                                        'check_period': '',
                                        'state': '0',
                                        'checks_enabled': '1',
                                        'name': 'DREI',
                                        'contacts': 'check_mk,hh',
                                        'notification_period': '24X7',
                                        'last_state_change': '1255301431',
                                        'notes': '',
                                        'check_command':
                                        'check-mk-ping',
                                        'acknowledged': '0',
                                        'in_notification_period': '1',
                                        'last_check': '1256194120',
                                        'alias': 'DREI',
                                        'action_url': '/nagios/pnp/index.php?host=$HOSTNAME$',
                                        'in_check_period': '1',
                                        'notes_url': '',
                                        'address': '127.0.0.1',
                                        'is_flapping': '0',
                                        'scheduled_downtime_depth': '0',
                                        'total_services': '1'
                                    },
                                    'Drei': {
                                        'check_period': '',
                                        'state': '0',
                                        'checks_enabled': '1',
                                        'name': 'Drei',
                                        'contacts': 'check_mk,hh',
                                        'notification_period': '24X7',
                                        'last_state_change': '1255301435',
                                        'notes': '',
                                        'check_command': 'check-mk-ping',
                                        'acknowledged': '0',
                                        'in_notification_period': '1',
                                        'last_check': '1256194120',
                                        'alias': 'Drei',
                                        'action_url': '/nagios/pnp/index.php?host=$HOSTNAME$',
                                        'in_check_period': '1',
                                        'notes_url': '',
                                        'address': '127.0.0.1',
                                        'is_flapping': '0',
                                        'scheduled_downtime_depth': '0',
                                        'total_services': '4'
                                    }
                                })

