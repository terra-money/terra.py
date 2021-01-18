import os
import sys

import pytest
import rstr

from terra_sdk import Terra
from terra_sdk.core.auth.transaction import StdFee
from terra_sdk.key.mnemonic import MnemonicKey

sys.path.append(os.path.join(os.path.dirname(__file__), "helpers"))  # isort:skip


# Set up testing environment
os.environ["terra_sdk_BECH32_VALIDATE"] = "0"

pytest.register_assert_rewrite("testtools")
from testtools import (  # isort:skip
    load_data,
    lcd_request_test_middleware,
)

# Config


def pytest_addoption(parser):
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


# Fixtures


@pytest.fixture(scope="session")
def tdd():  # short for test data dir
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


@pytest.fixture
def acc_address():
    return rstr.xeger(r"^terra[0-9a-z]{39}\Z")


@pytest.fixture
def make_acc_address():
    return lambda: rstr.xeger(r"^terra[0-9a-z]{39}\Z")


@pytest.fixture
def val_address():
    return rstr.xeger(r"^terravaloper[0-9a-z]{39}\Z")


@pytest.fixture
def make_val_address():
    return lambda: rstr.xeger(r"^terravaloper[0-9a-z]{39}\Z")


@pytest.fixture
def mnemonics(tdd):
    """Loads a series of known mnemonics and their generated addresses on account 0, index 0."""
    return load_data(tdd, "mnemonics.json")


@pytest.fixture(autouse=True, scope="session")
def mock_terra():
    """Mocks the Terra instance before a request is made."""
    terra = Terra("soju-0013", "")
    terra.lcd.request_middlewares.append(lcd_request_test_middleware)
    return terra


@pytest.fixture
def terra():
    """Testnet Terra connection."""
    return Terra("soju-0013", "https://soju-lcd.terra.dev")


@pytest.fixture
def wallet(mnemonics, terra):
    """Wallet #1, which should have some testnet funds."""
    m = mnemonics[0]["mnemonic"]
    return terra.wallet(MnemonicKey(m))


@pytest.fixture
def fee():
    return StdFee.make(gas=1000000, uluna=1000000)  # to make sure tx passes
