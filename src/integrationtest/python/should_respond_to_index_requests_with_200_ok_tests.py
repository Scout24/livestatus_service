import unittest
import urllib2

from liveserver import LiveServer


class Test(unittest.TestCase):

    def test(self):
        with LiveServer() as liveserver:
            response = urllib2.urlopen(liveserver.url)
            self.assertEquals(response.code, 200)


if __name__ == '__main__':
    unittest.main()
