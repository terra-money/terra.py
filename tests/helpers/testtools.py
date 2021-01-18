"""Quick and dirty scripts to load testing data and check serdes consistency and exactness."""

import json
import os
from pathlib import Path

import pytest

from terra_sdk.client.lcd.lcdrequest import LcdRequest


def load_data(testdatadir: str, filepath: str):
    return json.load(open(os.path.join(testdatadir, filepath), "r"))


def extract_msgs(txinfos: list, whitelist: list = None):
    msgs = []
    for txinfo in txinfos:
        msgs += txinfo["tx"]["value"]["msg"]
    if whitelist:
        msgs = filter(lambda m: m["type"] in whitelist, msgs)
    return msgs


def load_msg_examples(testdatadir: str, msg_types: list) -> dict:
    examples = dict()
    for mt in msg_types:
        data = load_data(testdatadir, f"txinfo_by_msg/{mt.type}.json")
        examples[mt] = extract_msgs(data["txs"], whitelist=[mt.type])
    return examples


def load_stdtx_examples(testdatadir: str) -> dict:
    examples = []
    files = Path(os.path.join(testdatadir, "txinfo_by_msg")).rglob("*.json")
    for f in files:
        data = json.load(open(f, "r"))
        txinfos = data["txs"]
        for txinfo in txinfos:
            examples.append(txinfo["tx"])
    return examples


# API testing tools


class LcdRequestTest(Exception):
    """This helps us break out and report the request so we can
    check its value before making the actual request. To be used
    with the proper middleware installation in LcdClient.
    """

    def __init__(self, request: LcdRequest):
        Exception.__init__(self)
        self.method = request.method
        self.url = request.url
        self.kwargs = request.kwargs


def lcd_request_test_middleware(client, request: LcdRequest):
    """Exits execution before an actual request is made against the server.
    Used to check a generated request's value for testing."""
    raise LcdRequestTest(request)


## Custom assertions


def assert_serdes_consistent(klass, item):
    """Will attempt to deserialize an item, and check if serializing and
    deserializing again produces an equal object.
    """
    x = klass.deserialize(item)
    y = klass.deserialize(json.loads(x.to_json()))
    assert x == y


def assert_serdes_exact(klass, item):
    """Will attempt to deserialize an item, and check if serializing to JSON produces
    equivalent JSON.
    """
    x = klass.deserialize(item)
    output_json = json.loads(x.to_json())
    assert item == output_json
