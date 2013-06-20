__author__ = 'mwolf'

import unittest
from livestatus_service.webapp import dispatch_request


class WebappTests(unittest.TestCase):

    def test_should_use_dispatch_function(self):
        result = dispatch_request('foobar', lambda x: 'replaced')
        self.assertEquals(result, ('replaced\n', 200))

    def test_should_replace_new_lines_in_requests(self):
        result = dispatch_request('foo\\nbar\\nbuzz', lambda x: x)
        self.assertEquals(result, ('foo\nbar\nbuzz\n', 200))
