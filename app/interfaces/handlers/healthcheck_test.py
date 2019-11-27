from __future__ import absolute_import
import unittest
from healthcheck import healthCheckHandler

class TestHealthcheck(unittest.TestCase):
    """
    Base class
    """

    def test_ok(self):
        """
        Testing if healthcheck response is ok.
        """
        res = healthCheckHandler()
        self.assertEqual(res, 120)


if __name__ == '__main__':
    unittest.main()