import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis_jsonschema import from_schema

from terra_sdk.core.staking.delegation import Delegation, Redelegation, UnbondingDelegation
from testtools import assert_serdes_consistent, assert_serdes_exact, load_data


@pytest.fixture(scope="module")
def delgn_examples(tdd):
    return load_data(tdd, "objects/staking/Delegation.json")


@pytest.fixture(scope="module")
def udelgn_examples(tdd):
    return load_data(tdd, "objects/staking/UnbondingDelegation.json")


@pytest.fixture(scope="module")
def rdelgn_examples(tdd):
    return load_data(tdd, "objects/staking/Redelegation.json")


class TestDelegationSerdes:
    def test_schema_valid(self, delgn_examples):
        for d in delgn_examples:
            assert_serdes_consistent(Delegation, d)
            assert_serdes_exact(Delegation, d)

    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(d=from_schema(Delegation.__schema__))
    def test_schema(self, d):
        assert_serdes_consistent(Delegation, d)


class TestUnbondingDelegationSerdes:
    def test_schema_valid(self, udelgn_examples):
        for d in udelgn_examples:
            assert_serdes_consistent(UnbondingDelegation, d)
            assert_serdes_exact(UnbondingDelegation, d)

    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(d=from_schema(UnbondingDelegation.__schema__))
    def test_schema(self, d):
        assert_serdes_consistent(UnbondingDelegation, d)


class TestRedelegationSerdes:
    def test_schema_valid(self, rdelgn_examples):
        for d in rdelgn_examples:
            assert_serdes_consistent(Redelegation, d)
            assert_serdes_exact(Redelegation, d)

    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(d=from_schema(Redelegation.__schema__))
    def test_schema(self, d):
        assert_serdes_consistent(Redelegation, d)
