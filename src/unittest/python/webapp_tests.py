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
from livestatus_service.webapp import (validate_and_dispatch,
                                       validate_query,
                                       dispatch_request,
                                       handle_index,
                                       render_application_template,
                                       handle_command,
                                       handle_query)


class WebappTests(unittest.TestCase):

    def setUp(self):
        self.logger_patcher = patch('livestatus_service.webapp.LOGGER.error')
        self.logger_patcher.start()

    def tearDown(self):
        self.logger_patcher.stop()

    def test_should_use_dispatch_function(self):
        result = dispatch_request('foobar', lambda x: 'replaced')
        self.assertEqual(result, ('replaced\n', 200))

    def test_should_replace_new_lines_in_requests(self):
        result = validate_query('foo\\nbar\\nbuzz')
        self.assertEqual(result, 'foo\nbar\nbuzz')

    def test_should_respond_with_error_when_uncaught_exception_occurs(self):
        mock_request = Mock()
        mock_request.args.get.side_effect = ValueError('too fat to fly')

        response = validate_and_dispatch(mock_request, lambda x: None)

        self.assertEqual(response, ('Error : too fat to fly', 200))

    def test_should_raise_exception_when_query_is_missing(self):
        self.assertRaises(BaseException, validate_query, None)

    def test_should_raise_exception_when_query_specifies_an_outputformat(self):
        self.assertRaises(
            BaseException, validate_query, 'foo\nOutputFormat: json\nbar')

    @patch('livestatus_service.webapp.dispatch_request')
    def test_should_return_error_when_exception_is_raised(self, dispatch_request):
        mock_request = Mock()
        mock_args = {'q': 'foobar',
                     'handler': 'spam',
                     'key': 'bacon'}
        mock_request.args = mock_args

        concatenate_args = (lambda query, dispatch_function, **kwargs:
                            query +
                            dispatch_function +
                            kwargs['key'] +
                            kwargs['handler'])

        dispatch_request.side_effect = concatenate_args

        result = validate_and_dispatch(mock_request, 'noodles')

        self.assertEqual(result, 'foobarnoodlesbaconspam')

    @patch('livestatus_service.webapp.render_application_template')
    def test_handle_index_should_render_the_index_template(self, mock_render):
        handle_index()

        mock_render.assert_called_with('index.html')

    @patch('livestatus_service.webapp.render_template')
    def test_render_app_template_should_render_template_with_version(self, mock_render):
        render_application_template('index.html')

        mock_render.assert_called_with(
            'index.html', version=livestatus_service.__version__)

    @patch('livestatus_service.webapp.validate_and_dispatch')
    def test_handle_command_should_dispatch_with_perform_command(self, mock_dispatch):
        handle_command()

        mock_dispatch.assert_called_with(livestatus_service.webapp.request,
                                         livestatus_service.webapp.perform_command)

    @patch('livestatus_service.webapp.validate_and_dispatch')
    def test_handle_query_should_dispatch_with_perform_query(self, mock_dispatch):
        handle_query()

        mock_dispatch.assert_called_with(livestatus_service.webapp.request,
                                         livestatus_service.webapp.perform_query)
