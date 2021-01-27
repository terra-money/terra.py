from terra_sdk.core.auth import Account
import json


def test_deserializes_example():
    examples = json.load(open("./Account.data.json"))
    print(examples)