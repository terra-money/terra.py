import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st
from hypothesis_jsonschema import from_schema

from terra_sdk.core.msg.market import MsgSwap
from terra_sdk.core.sdk import Coin
from terra_sdk.error import InvalidAccAddress
from terra_sdk.util.validation import is_acc_address
from testtools import assert_serdes_consistent, assert_serdes_exact, load_msg_examples


@pytest.fixture(scope="module")
def msg_examples(tdd):
    """Stores the __schema__ validation set for market messages."""
    return load_msg_examples(tdd, msg_types=[MsgSwap],)


class TestMsgSwap:
    def test_schema_valid(self, msg_examples):
        for m in msg_examples[MsgSwap]:
            assert_serdes_consistent(MsgSwap, m)
            assert_serdes_exact(MsgSwap, m)

    @pytest.mark.serdes
    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(MsgSwap.__schema__))
    def test_serdes_consistent(self, m):
        assert_serdes_consistent(MsgSwap, m)

    def test_matches_meta(self):
        assert MsgSwap.type == "market/MsgSwap"
        assert MsgSwap.action == "swap"

    @given(other=st.text())
    def test_constructor_validates_addresses(self, acc_address, other):
        """MsgSwap should validate `trader` to be AccAddress.
        """
        assume(not is_acc_address(other))
        with pytest.raises(InvalidAccAddress):
            MsgSwap(trader=other, offer_coin=Coin("uluna", 100), ask_denom="umnt")
        A = MsgSwap(trader=acc_address, offer_coin=Coin("uluna", 100), ask_denom="umnt")
        assert A.trader == acc_address
