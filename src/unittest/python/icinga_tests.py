from __future__ import absolute_import

import unittest
from mock import patch, MagicMock, call

from livestatus_service.icinga import perform_command


class IcingaTests(unittest.TestCase):

    @patch('livestatus_service.icinga.open', create=True)
    @patch('livestatus_service.icinga.time.time')
    def test_should_write_command_in_correct_syntax_to_named_pipe(self, mock_time, mock_open):
        mock_open.return_value = MagicMock(spec=file)
        mock_time.return_value = '123'

        perform_command('FOO;bar', '/path/to/commandfile.cmd', None)

        self.assertEqual(mock_open.call_args, call('/path/to/commandfile.cmd', 'w'))
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.write.assert_called_with('[123] FOO;bar\n')
