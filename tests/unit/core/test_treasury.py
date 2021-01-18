import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from hypothesis_jsonschema import from_schema

from terra_sdk.core import Coin, Dec
from terra_sdk.core.treasury import PolicyConstraints
from testtools import assert_serdes_consistent, assert_serdes_exact


@pytest.fixture
def default_tax_policy():
    return PolicyConstraints(
        rate_min=Dec.with_prec(5, 4),
        rate_max=Dec.with_prec(1, 2),
        cap=Coin("usdr", 1),
        change_max=Dec.with_prec(25, 5),
    )


@pytest.fixture
def default_tax_rate():
    return Dec.with_prec(1, 3)


class TestPolicyConstraints:
    @pytest.mark.serdes
    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(PolicyConstraints.__schema__))
    def test_serdes_consistent(self, m):
        assert_serdes_consistent(PolicyConstraints, m)

    def test_clamp(self, default_tax_policy, default_tax_rate):
        # Analogous test:
        # https://github.com/terra-project/core/blob/develop/x/treasury/internal/types/constraint_test.go#L10
        tax_policy = default_tax_policy
        prev_rate = default_tax_rate

        # Case 1: try to update delta > change_max
        new_rate = prev_rate + tax_policy.change_max * 2
        clamped_rate = tax_policy.clamp(prev_rate, new_rate)
        assert prev_rate + tax_policy.change_max == clamped_rate

        # Case 2: try to update delta > change_max (negative)
        new_rate = prev_rate - tax_policy.change_max * 2
        clamped_rate = tax_policy.clamp(prev_rate, new_rate)
        assert prev_rate - tax_policy.change_max == clamped_rate

        # Case 3: try to update the new rate > min_rate
        prev_rate = tax_policy.rate_max
        new_rate = prev_rate + Dec.with_prec(1, 3)
        clamped_rate = tax_policy.clamp(prev_rate, new_rate)
        assert tax_policy.rate_max == clamped_rate

        # Case 4: try to update the new rate < minRate
        prev_rate = tax_policy.rate_min
        new_rate = tax_policy.rate_min - Dec.with_prec(1, 3)
        clamped_rate = tax_policy.clamp(prev_rate, new_rate)
        assert tax_policy.rate_min == clamped_rate
