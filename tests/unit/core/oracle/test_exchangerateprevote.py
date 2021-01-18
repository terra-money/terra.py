import json

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis_jsonschema import from_schema

from terra_sdk.core.oracle import ExchangeRatePrevote
from testtools import assert_serdes_consistent, assert_serdes_exact, load_data


@pytest.fixture
def examples(tdd):
    return load_data(tdd, "objects/oracle/ExchangeRatePrevote.json")


class TestExchangeRatePrevoteSerdes:
    def test_schema_valid(self, examples):
        for x in examples:
            assert_serdes_consistent(ExchangeRatePrevote, x)
            assert_serdes_exact(ExchangeRatePrevote, x)

    @pytest.mark.serdes
    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow])
    @given(x=from_schema(ExchangeRatePrevote.__schema__))
    def test_serdes_consistent(self, x):
        assert_serdes_consistent(ExchangeRatePrevote, x)
