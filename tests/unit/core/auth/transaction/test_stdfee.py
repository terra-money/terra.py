import json

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from hypothesis_jsonschema import from_schema

from terra_sdk.core.auth.transaction import StdFee


class TestStdFeeSerdes:
    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(fee=from_schema(StdFee.__schema__))
    def test_schema(self, fee):
        x = StdFee.deserialize(fee)
        y = StdFee.deserialize(json.loads(x.to_json()))
        assert x == y
