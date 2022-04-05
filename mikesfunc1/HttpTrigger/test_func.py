import unittest
import azure.functions as func

# import azure.functions_worker.bindings as bindings
import azure_functions_worker.bindings as bindings
from . import main


class TestFunction(unittest.TestCase):
    def test_name(self):
        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method="GET", body=None, url="/HttpTrigger", params={"name": "Test"}
        )
        trace = bindings.TraceContext("parent", "state", {})
        context = bindings.Context("test_name", "HttpTrigger", "123", trace)

        # Call the function.
        resp = main(req, context)
        # print(resp.get_body())

        # Check the output.
        self.assertIn(
            b'test_name says: Hello Test!\nContext:\n{\n  "function_directory": "HttpTrigger",\n  "function_name": "test_name",\n  "invocation_id": "123"\n}',
            resp.get_body(),
        )
