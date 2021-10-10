import unittest
import azure.functions as func
from . import main


class TestFunction(unittest.TestCase):
    def test_name(self):
        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method="GET", body=None, url="/webhooks", params={"name": "Test"}
        )

        # Call the function.
        resp = main(req)
        # print(resp.get_body())

        # Check the output.
        self.assertEqual(resp.get_body(), b"Hello Test!")
