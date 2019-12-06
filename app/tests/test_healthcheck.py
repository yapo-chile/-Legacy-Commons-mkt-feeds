import unittest
from app import APP

TEST_APP = APP.test_client()
URL = '/healthcheck'


class TestHealthcheck(unittest.TestCase):
    def test_healthcheck_OK(self):
        # Make a test request to healthcheck
        response = TEST_APP.get(URL)

        # Assert response status 200 OK.
        self.assertEqual(response.status, "200 OK")

        # Assert response body
        self.assertEqual(response.json, {"status": "OK"})

    def test_healthcheck_BadRequest(self):
        # Make a test request to healthcheck
        response = TEST_APP.post(URL)

        # Assert response status METHOD NOT ALLOWED.
        self.assertEqual(response.status, "405 METHOD NOT ALLOWED")
