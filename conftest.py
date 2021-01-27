import pytest

from pathlib import Path
import json


@pytest.fixture(scope="session")
def load_json_examples():
    def _load(pathlocal, file):
        return json.load(open(Path(pathlocal).parent / file))

    return _load
