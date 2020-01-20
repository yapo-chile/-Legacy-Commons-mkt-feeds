import unittest
from app import APP

TEST_APP = APP.test_client()
URL = '/catalog/get'


class TestCatalog(unittest.TestCase):
    def test_Catalog_OK(self):
        # Make a test request to catalog
        response = TEST_APP.get(URL + "/1")

        # Assert response status 200 OK.
        self.assertEqual(response.status, "200 OK")

    def test_catalog_BadRequests(self):
        # Assert response status 404.
        self.assertEqual(TEST_APP.post(URL).status, "404 NOT FOUND")

        # Assert response status 404.
        self.assertEqual(
            TEST_APP.post(
                URL + "/1").status,
            "405 METHOD NOT ALLOWED")
