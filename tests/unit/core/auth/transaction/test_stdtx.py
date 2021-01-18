import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from hypothesis_jsonschema import from_schema

from terra_sdk.core.auth.transaction import StdTx
from terra_sdk.core.sdk import Coin
from testtools import assert_serdes_consistent, assert_serdes_exact, load_stdtx_examples


@pytest.fixture(scope="module")
def examples(tdd):
    # need to create the data by looking inside txinfo
    return load_stdtx_examples(tdd)


class TestStdTxSerdes:
    def test_schema_valid(self, examples):
        for tx in examples:
            assert_serdes_consistent(StdTx, tx)
            # assert_serdes_exact(StdTx, tx)
            # Cannot be exact due to inability to preserve json order

    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(tx=from_schema(StdTx.__schema__))
    def test_serdes_consistent(self, tx):
        assert_serdes_consistent(StdTx, tx)
