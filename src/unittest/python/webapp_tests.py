__author__ = 'mwolf'

import unittest
from mockito import when, unstub, any, mock
import livestatus_service
from livestatus_service.webapp import dispatch_request,\
                                      validate_and_dispatch,\
                                      validate_query,\
                                      handle_index


class WebappTests(unittest.TestCase):

    def tearDown(self):
        unstub()

    def setUp(self):
        when(livestatus_service.webapp.LOGGER).error(any()).thenReturn(None)

    def test_should_use_dispatch_function(self):
        result = dispatch_request('foobar', lambda x: 'replaced')
        self.assertEquals(result, ('replaced\n', 200))

    def test_should_replace_new_lines_in_requests(self):
        result = validate_query('foo\\nbar\\nbuzz')
        self.assertEquals(result, 'foo\nbar\nbuzz')

    def test_should_respond_with_error_when_uncaught_exception_occurs(self):
        mock_request = mock()
        mock_args = mock()
        mock_request.args = mock_args
        when(mock_args).get(any()).thenRaise(ValueError('too fat to fly'))

        response = validate_and_dispatch(mock_request, lambda x: None)

        self.assertEquals(response, ('Error : too fat to fly', 500))

    def test_should_raise_exception_when_query_is_missing(self):
        self.assertRaises(BaseException, validate_query, None)

    def test_should_return_error_when_exception_is_raised(self):
        mock_request = mock()
        mock_args = {'q': 'foobar',
                     'handler': 'spam',
                     'key': 'bacon'}
        mock_request.args = mock_args
        concatenate_args = lambda query, dispatch_function, **kwargs : query + dispatch_function + kwargs['key'] + kwargs['handler']

        livestatus_service.webapp.dispatch_request = concatenate_args

        result = validate_and_dispatch(mock_request, 'noodles')

        self.assertEquals(result, 'foobarnoodlesbaconspam')
