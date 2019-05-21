import unittest
import azure.functions as func
import azure.functions_worker.bindings as bindings
from . import main


class TestFunction(unittest.TestCase):
    def test_name(self):
        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/HttpTrigger', 
            params={'name': 'Test'})
        context = bindings.Context(
            'test_name',
            'HttpTrigger',
            '123'
        )

        # Call the function.
        resp = main(req, context)
        #print(resp.get_body())

        # Check the output.
        self.assertEqual(
            resp.get_body(),
            b'test_name says: Hello Test!\nContext:\n{\n  "function_directory": "HttpTrigger",\n  "function_name": "test_name",\n  "invocation_id": "123"\n}'
        )
