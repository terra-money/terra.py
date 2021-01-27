import pytest

from pathlib import Path
import json


def _load(pathlocal, file):
    return json.load(open(Path(pathlocal).parent / file))


def _load_msg_examples(msgtype, pathlocal, file):
    examples = []
    data = _load(pathlocal, file)
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
