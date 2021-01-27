import pytest

from pathlib import Path
import json


def _load(file):
    return json.load(open(Path(__file__).parent / "data" / file))


def _load_msg_examples(msgtype, file):
    examples = []
    data = _load(file)
    for tx_info in data["txs"]:
        for msg in tx_info["tx"]["value"]["msg"]:
            if msg["type"] == msgtype:
                examples.append(msg)
    return examples


@pytest.fixture(scope="session")
def load_json_examples():
    return _load


@pytest.fixture(scope="session")
def load_msg_examples():
    return _load_msg_examples
