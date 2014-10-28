# -*- coding: utf-8 -*-

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
from mock import patch, MagicMock, call
import unittest

try:
    import io
    file = io.IOBase  # file is IOBase in python3
except ImportError:
    pass

from livestatus_service.icinga import perform_command


class IcingaTests(unittest.TestCase):

    @patch('livestatus_service.icinga.open', create=True)
    @patch('livestatus_service.icinga.time.time')
    def test_should_write_command_in_correct_syntax_to_named_pipe(self, mock_time, mock_open):
        mock_open.return_value = MagicMock(spec=file)
        mock_time.return_value = '123'

        perform_command('FOO;bar', '/path/to/commandfile.cmd')

        self.assertEqual(mock_open.call_args, call('/path/to/commandfile.cmd', 'w'))
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.write.assert_called_with(b'[123] FOO;bar\n')

    @patch('livestatus_service.icinga.open', create=True)
    @patch('livestatus_service.icinga.time.time')
    def test_should_write_utf8_command_to_named_pipe(self, mock_time, mock_open):
        mock_open.return_value = MagicMock(spec=file)
        mock_time.return_value = '123'

        perform_command('FOO;bär', '/path/to/commandfile.cmd')

        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.write.assert_called_with(b'[123] FOO;bär\n')
