import logging
import azure.functions as func
import json


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        # find public attributes for context = ABC
        attrlist = [attr for attr in dir(context) if not attr.startswith('_')]
        info = {}
        for attr in attrlist:
            if attr == 'trace_context':
                # info[attr] = getattr(context, attr).__dict__
                continue
            info[attr] = getattr(context, attr)
        dump = json.dumps(info, indent=2, default=lambda o: repr(o))
        return func.HttpResponse(f"{context.function_name} says: Hello {name}!\nContext:\n{dump}")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
