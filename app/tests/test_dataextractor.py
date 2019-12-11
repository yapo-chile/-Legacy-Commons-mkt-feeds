import unittest
from app import APP

TEST_APP = APP.test_client()
URL = '/dataExtractor'


class TestDataExtractor(unittest.TestCase):
    def test_DataExtractor_OK(self):
        # Make a test request to catalog
        response = TEST_APP.get(URL)

        # Assert response status 200 OK.
        self.assertEqual(response.status, "200 OK")

    def test_DataExtractor_BadRequests(self):
        # Assert response status 404.
        self.assertEqual(TEST_APP.post(URL).status, "404 NOT FOUND")

        # Assert response status 404.
        self.assertEqual(
            TEST_APP.post(URL).status, "405 METHOD NOT ALLOWED")
