import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis_jsonschema import from_schema

from terra_sdk.core.staking.validator import Validator
from testtools import assert_serdes_consistent, assert_serdes_exact, load_data


@pytest.fixture(scope="module")
def examples(tdd):
    return load_data(tdd, "objects/staking/Validator.json")


class TestValidatorSerdes:
    def test_schema_valid(self, examples):
        for v in examples:
            assert_serdes_consistent(Validator, v)
            assert_serdes_exact(Validator, v)

    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(v=from_schema(Validator.__schema__))
    def test_serdes_consistent(self, v):
        assert_serdes_consistent(Validator, v)
