import unittest
import azure.functions as func

# import azure.functions_worker.bindings as bindings
#import azure_functions_worker.bindings as bindings
from azure.functions._abc import TraceContext, RetryContext
import threading
from . import main


class TestFunction(unittest.TestCase):
    def test_name(self):
        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method="GET", body=None, url="/HttpTrigger", params={"name": "Test"}
        )
        #trace = bindings.TraceContext("parent", "state", {})
        #context = bindings.Context("test_name", "HttpTrigger", "123", trace)
        context = self._generate_func_context()

        # Call the function.
        resp = main(req, context)
        # print(resp.get_body())

        # Check the output.
        self.assertIn(
            b'test_name says: Hello Test!\nContext:\n{\n  "function_directory": "HttpTrigger",\n  "function_name": "test_name",\n  "invocation_id": "123",\n',
            resp.get_body(),
        )

    # Source: https://github.com/Azure/azure-functions-python-library/blob/dev/tests/test_http_wsgi.py
    def _generate_func_context(
        self,
        invocation_id='123',
        thread_local_storage=threading.local(),
        function_name='test_name',
        function_directory='HttpTrigger',
        trace_context=TraceContext,
        retry_context=RetryContext
    ) -> func.Context:
        class MockContext(func.Context):
            def __init__(self, ii, tls, fn, fd, tc, rc):
                self._invocation_id = ii
                self._thread_local_storage = tls
                self._function_name = fn
                self._function_directory = fd
                self._trace_context = tc
                self._retry_context = rc

            @property
            def invocation_id(self):
                return self._invocation_id

            @property
            def thread_local_storage(self):
                return self._thread_local_storage

            @property
            def function_name(self):
                return self._function_name

            @property
            def function_directory(self):
                return self._function_directory

            @property
            def trace_context(self):
                return self._trace_context

            @property
            def retry_context(self):
                return self._retry_context

        return MockContext(invocation_id, thread_local_storage,
                           function_name, function_directory,
                           trace_context, retry_context)

