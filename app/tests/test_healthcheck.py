import unittest
from app import app

TEST_APP = app.test_client()
URL = '/healthcheck'

class TestHealthcheck(unittest.TestCase):
    def test_healthcheck_OK(self):
        # Make a test request to healthcheck
        response = TEST_APP.get(URL)

        # Assert response status 200 OK.                                           
        self.assertEquals(response.status, "200 OK")

        # Assert response body
        self.assertEquals(response.json, {"status": "OK"})
    
    def test_healthcheck_BadRequest(self):
        # Make a test request to healthcheck
        response = TEST_APP.post(URL)

        # Assert response status METHOD NOT ALLOWED.                                           
        self.assertEquals(response.status, "405 METHOD NOT ALLOWED")
