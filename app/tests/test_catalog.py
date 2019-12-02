import unittest
from app import app

TEST_APP = app.test_client()
URL = '/catalog'

class TestCatalog(unittest.TestCase):
    def test_Catalog_OK(self):
        # Make a test request to catalog
        response = TEST_APP.get(URL+"/1")

        # Assert response status 200 OK.                                           
        self.assertEquals(response.status, "200 OK")

        # Missing assert file output
        # Missing assert logs
    
    def test_catalog_BadRequests(self):
        # Assert response status 404.                                           
        self.assertEquals(TEST_APP.post(URL).status, "404 NOT FOUND")

        # Assert response status 404.                                           
        self.assertEquals(TEST_APP.post(URL+"/1").status, "405 METHOD NOT ALLOWED")
