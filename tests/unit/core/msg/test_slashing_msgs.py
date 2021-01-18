import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st
from hypothesis_jsonschema import from_schema

from terra_sdk.core.msg.slashing import MsgUnjail
from terra_sdk.error import InvalidValAddress
from terra_sdk.util.validation import is_val_address
from testtools import assert_serdes_consistent, assert_serdes_exact, load_msg_examples


@pytest.fixture(scope="module")
def msg_examples(tdd):
    """Stores the __schema__ validation set for slashing messages."""
    return load_msg_examples(tdd, msg_types=[MsgUnjail],)


class TestMsgUnjail:
    def test_schema_valid(self, msg_examples):
        for m in msg_examples[MsgUnjail]:
            assert_serdes_consistent(MsgUnjail, m)
            assert_serdes_exact(MsgUnjail, m)

    @pytest.mark.serdes
    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(MsgUnjail.__schema__))
    def test_schema(self, m):
        assert_serdes_consistent(MsgUnjail, m)

    def test_matches_meta(self):
        assert MsgUnjail.type == "cosmos/MsgUnjail"
        assert MsgUnjail.action == "unjail"

    @given(other=st.text())
    def test_constructor_validates_addresses(self, val_address, other):
        """MsgUnjail should validate `address` to be ValAddress.
        """
        assume(not is_val_address(other))
        with pytest.raises(InvalidValAddress):
            MsgUnjail(address=other)
        A = MsgUnjail(address=val_address)
        assert A.address == val_address
