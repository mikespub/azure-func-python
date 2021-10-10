import logging
import azure.functions as func
from azure.appconfiguration import AzureAppConfigurationClient, ConfigurationSetting
import os
import json


# define route with optional params in function.json: appconfig/{label?}/{key?}/{attrib?}
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")
    if len(req.route_params) > 0:
        logging.info("Route params: %s" % req.route_params)
    CONNECTION_STRING = get_connection_string()
    if not CONNECTION_STRING:
        return func.HttpResponse("AZURE_APPCONFIG_CONNECTION_STRING must be set.")
    # Create app config client
    client = AzureAppConfigurationClient.from_connection_string(CONNECTION_STRING)

    label = req.route_params.get("label")
    if not label:
        label = req.params.get("label")
    if not label:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            label = req_body.get("label")

    key = req.route_params.get("key")
    if not key:
        key = req.params.get("key")
    if not key:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            key = req_body.get("key")

    if label:
        if key:
            config_settings = client.list_configuration_settings(
                labels=[label], keys=[key]
            )
            items = []
            # find public attributes for ConfigurationSetting = Model
            # attrlist = [attr for attr in dir(context) if not attr.startswith('_')]
            attrib = req.route_params.get("attrib")
            for item in config_settings:
                info = dict(item.__dict__)
                if "AccountKey=" in info["value"] or "PASSWORD" in info["key"].upper():
                    info["value"] = "(hidden value)"
                if attrib and attrib in info:
                    dump = info[attrib]
                    return func.HttpResponse(
                        f"Label: {label}\nKey: {key}\nAttribute: {attrib}\n{dump}"
                    )
                items.append(info)
            dump = json.dumps(items, indent=2, default=lambda o: repr(o))
            return func.HttpResponse(f"Label: {label}\nKey: {key}\nAttributes:\n{dump}")
        config_settings = client.list_configuration_settings(labels=[label])
        items = []
        for item in config_settings:
            items.append(item.key)
        dump = json.dumps(items, indent=2, default=lambda o: repr(o))
        return func.HttpResponse(f"Label: {label}\nKeys:\n{dump}")
    else:
        config_settings = client.list_configuration_settings()
        labels = {}
        for item in config_settings:
            if item.label not in labels:
                labels[item.label] = 0
            labels[item.label] += 1
        dump = json.dumps(labels, indent=2)
        return func.HttpResponse(f"Labels:\n{dump}")


# https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/appconfiguration/azure-appconfiguration/samples
def get_connection_string():
    try:
        CONNECTION_STRING = os.environ["AZURE_APPCONFIG_CONNECTION_STRING"]
        return CONNECTION_STRING
    except KeyError:
        print("AZURE_APPCONFIG_CONNECTION_STRING must be set.")
        return
