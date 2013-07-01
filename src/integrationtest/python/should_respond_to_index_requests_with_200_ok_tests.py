import unittest
try:
    from urllib2 import urlopen
except:
    from urllib.request import urlopen

from liveserver import LiveServer


class Test(unittest.TestCase):

    def test(self):
        with LiveServer() as liveserver:
            response = urlopen(liveserver.url)
            self.assertEquals(response.code, 200)


if __name__ == '__main__':
    unittest.main()
