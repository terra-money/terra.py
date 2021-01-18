import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis_jsonschema import from_schema

from terra_sdk.core.auth.account import Account
from testtools import assert_serdes_consistent, assert_serdes_exact, load_data


@pytest.fixture
def examples(tdd):
    return load_data(tdd, "objects/auth/Account.json")


class TestAccountSerdes:
    def test_schema_valid(self, examples):
        for acc in examples:
            assert_serdes_consistent(Account, acc)
            assert_serdes_exact(Account, acc)

    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(acc=from_schema(Account.__schema__))
    def test_serdes_consistent(self, acc):
        assert_serdes_consistent(Account, acc)
