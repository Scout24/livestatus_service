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

from mock import patch, call, PropertyMock
import unittest

import livestatus_service
from livestatus_service import initialize_logging


class LivestatusServiceInitializationTests(unittest.TestCase):

    @patch('livestatus_service.initialize_logging')
    @patch('livestatus_service.Configuration')
    def test_should_initialize_logging_with_current_configuration(self, mock_config, mock_initialize_logging):
        config_properties = PropertyMock()
        config_properties.log_file = '/foo/bar/baz.log'
        mock_config.return_value = config_properties


        livestatus_service.initialize('/foo/bar/config.cfg')

        self.assertEquals(mock_initialize_logging.call_args, call(config_properties.log_file))

    @patch('livestatus_service.logging.FileHandler')
    def test_initialize_logging_should_create_log_file_handler(self, mock_file_handler):
        initialize_logging('/path/to/log/file')

        self.assertEquals(mock_file_handler.call_args, call('/path/to/log/file'))
