import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis_jsonschema import from_schema

from terra_sdk.core.auth.account import LazyGradedVestingAccount
from testtools import assert_serdes_consistent, assert_serdes_exact, load_data


@pytest.fixture
def examples(tdd):
    return load_data(tdd, "objects/auth/LazyGradedVestingAccount.json")


class TestVestingAccountSerdes:
    def test_schema_valid(self, examples):
        for acc in examples:
            assert_serdes_consistent(LazyGradedVestingAccount, acc)
            assert_serdes_exact(LazyGradedVestingAccount, acc)

    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(acc=from_schema(LazyGradedVestingAccount.__schema__))
    def test_schema(self, acc):
        assert_serdes_consistent(LazyGradedVestingAccount, acc)
