import json

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis_jsonschema import from_schema

from terra_sdk.core.oracle import ExchangeRateVote
from testtools import assert_serdes_consistent, assert_serdes_exact, load_data


@pytest.fixture
def examples(tdd):
    return load_data(tdd, "objects/oracle/ExchangeRateVote.json")


class TestExchangeRateVoteSerdes:
    def test_schema_valid(self, examples):
        for x in examples:
            assert_serdes_consistent(ExchangeRateVote, x)
            assert_serdes_exact(ExchangeRateVote, x)

    @pytest.mark.serdes
    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow])
    @given(x=from_schema(ExchangeRateVote.__schema__))
    def test_serdes_consistent(self, x):
        assert_serdes_consistent(ExchangeRateVote, x)
