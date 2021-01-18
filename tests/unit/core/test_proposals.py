import json

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from hypothesis_jsonschema import from_schema

from terra_sdk.core.proposal import (
    CommunityPoolSpendProposal,
    ParameterChangeProposal,
    RewardWeightUpdateProposal,
    TaxRateUpdateProposal,
    TextProposal,
)
from testtools import assert_serdes_consistent, assert_serdes_exact


class TestTextProposal:
    @pytest.mark.serdes
    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(TextProposal.__schema__))
    def test_serdes_consistent(self, m):
        assert_serdes_consistent(TextProposal, m)

    def test_matches_meta(self):
        assert TextProposal.type == "gov/TextProposal"


class TestTaxRateUpdateProposal:
    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(TaxRateUpdateProposal.__schema__))
    def test_serdes_consistent(self, m):
        assert_serdes_consistent(TaxRateUpdateProposal, m)

    def test_matches_meta(self):
        assert TaxRateUpdateProposal.type == "treasury/TaxRateUpdateProposal"


class TestRewardWeightUpdateProposal:
    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(RewardWeightUpdateProposal.__schema__))
    def test_serdes_consistent(self, m):
        assert_serdes_consistent(RewardWeightUpdateProposal, m)

    def test_matches_meta(self):
        assert RewardWeightUpdateProposal.type == "treasury/RewardWeightUpdateProposal"


class TestCommunityPoolSpendProposal:
    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(CommunityPoolSpendProposal.__schema__))
    def test_serdes_consistent(self, m):
        assert_serdes_consistent(CommunityPoolSpendProposal, m)

    def test_matches_meta(self):
        assert (
            CommunityPoolSpendProposal.type == "distribution/CommunityPoolSpendProposal"
        )


class TestParameterChangeProposal:
    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(ParameterChangeProposal.__schema__))
    def test_serdes_consistent(self, m):
        assert_serdes_consistent(ParameterChangeProposal, m)

    def test_matches_meta(self):
        assert ParameterChangeProposal.type == "params/ParameterChangeProposal"
