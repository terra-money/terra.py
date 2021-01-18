# Request middlewares
import json
import re

import requests

from terra_sdk.error import BadRequest, LcdInternalError, get_codespace_error, get_rpc_error
from terra_sdk.util.serdes import serialize_to_json

from .lcdrequest import LcdRequest

__all__ = [
    "set_timeout",
    "set_query",
    "handle_codespace_errors",
    "handle_general_errors",
]


def set_timeout(client, request: requests.Request):
    kwargs = request.kwargs
    kwargs["timeout"] = kwargs.get("timeout", client.timeout)
    return LcdRequest(request.method, request.url, kwargs)


def set_query(client, request: requests.Request):
    """Add `params` to GET requests to make queries, and `data` to POST requests for
    submitting JSON data. Applies serialization strategy to JSON post requests."""

    method = request.method
    kwargs = request.kwargs
    kwargs["data"] = kwargs.get("data", None)
    kwargs["headers"] = kwargs.get("headers", {})

    if kwargs["data"] and method == "get":
        kwargs["params"] = kwargs["data"]
        del kwargs["data"]

    if method == "post":
        kwargs["headers"]["content-type"] = "application/json"
        kwargs["data"] = serialize_to_json(kwargs["data"])  # apply custom serialization
    return LcdRequest(method, request.url, kwargs)


# Response middlewares
def handle_codespace_errors(client, response: requests.Response):
    """Try to extract more specific codespace errors."""
    error_type = str(response.status_code)[0]
    if error_type in ["4", "5"]:
        try:
            res = response.json()
            error = res.get("error", "")
            if isinstance(error, dict):
                error_msg = error["message"]
            else:
                error_msg = error
        except (ValueError, TypeError, KeyError):
            error_msg = response.content
        try:
            e = json.loads(error_msg)
            if isinstance(e, dict) and "codespace" in e:
                raise get_codespace_error(e["codespace"], e["code"], e["message"])
        except json.decoder.JSONDecodeError:
            pass  # continue normally
    return response


def handle_general_errors(client, response: requests.Response):
    """Handles 4xx and 5xx errors. Checks first if they originally from an RPC error."""
    error_type = str(response.status_code)[0]
    if error_type in ["4", "5"]:
        try:
            res = response.json()
            error = res.get("error", {})
            if isinstance(error, dict):
                error_msg = error["message"]
            else:
                error_msg = error
        except (ValueError, TypeError, KeyError):
            error_msg = response.content
        match = re.match(r"^.*RPC error (\-?\d+) - (.*)$", str(error_msg))
        if match:
            raise get_rpc_error(int(match.group(1)), match.group(2), response.request)
        if error_type == "4":
            raise BadRequest(response.status_code, error_msg, response.request)
        if error_type == "5":
            raise LcdInternalError(response.status_code, error_msg, response.request)
    return response
