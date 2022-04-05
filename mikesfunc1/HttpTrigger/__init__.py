import json
import logging
import os
import socket
import sys
import time

import azure.functions as func


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    name = req.params.get("name")
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get("name")

    if name:
        # find public attributes for context = ABC
        attrlist = [attr for attr in dir(context) if not attr.startswith("_")]
        info = {}
        for attr in attrlist:
            if attr == "trace_context":
                # info[attr] = getattr(context, attr).__dict__
                continue
            info[attr] = getattr(context, attr)
        dump = json.dumps(info, indent=2, default=lambda o: repr(o))
        env = dict(os.environ)
        for k in env:
            if k.endswith("_CONNECTION_STRING") or k.endswith("_KEY"):
                env[k] = "(private)"
                continue
            if "AccountKey" in env[k]:
                env[k] = "(private)"
                continue
        info = json.dumps(env, indent=2, default=lambda o: repr(o), sort_keys=True)
        # return "Hello world from {}:<pre>{}</pre>".format(
        #     __file__, escape(info)
        # )
        tmpl = (
            "{func_name} says: Hello {name}!\n"
            "Context:\n{dump}\n"
            "Hostname: {hostname}\n"
            "File: {file}\n"
            "Modified: {date}\n"
            "Python: {version}\n"
            "Environ:\n{environ}\n"
        )
        return func.HttpResponse(
            tmpl.format(
                func_name=context.function_name,
                name=name,
                dump=dump,
                hostname=socket.gethostname(),
                file=__file__,
                date=time.ctime(os.path.getmtime(__file__)),
                version=sys.version,
                environ=info,
            )
        )
        # return func.HttpResponse(
        #     f"{context.function_name} says: Hello {name}!\nContext:\n{dump}"
        # )
    else:
        return func.HttpResponse(
            "Please pass a name on the query string or in the request body",
            status_code=400,
        )
