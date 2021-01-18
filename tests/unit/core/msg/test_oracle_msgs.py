from decimal import Decimal

import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st
from hypothesis_jsonschema import from_schema

from terra_sdk.core.msg.oracle import (
    MsgDelegateFeedConsent,
    MsgExchangeRatePrevote,
    MsgExchangeRateVote,
)
from terra_sdk.core.sdk import Coin, Dec
from terra_sdk.error import InvalidAccAddress, InvalidValAddress, ValidationError
from terra_sdk.util.validation import is_acc_address, is_val_address
from testtools import assert_serdes_consistent, assert_serdes_exact, load_msg_examples


@pytest.fixture(scope="module")
def msg_examples(tdd):
    """Stores the __schema__ validation set for oracle messages."""
    return load_msg_examples(
        tdd,
        msg_types=[MsgDelegateFeedConsent, MsgExchangeRateVote, MsgExchangeRatePrevote],
    )


class TestMsgExchangeRateVote:
    def test_schema_valid(self, msg_examples):
        for m in msg_examples[MsgExchangeRateVote]:
            assert_serdes_consistent(MsgExchangeRateVote, m)
            assert_serdes_exact(MsgExchangeRateVote, m)

    @pytest.mark.serdes
    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(MsgExchangeRateVote.__schema__))
    def test_serdes_consistent(self, m):
        assert_serdes_consistent(MsgExchangeRateVote, m)

    def test_matches_meta(self):
        assert MsgExchangeRateVote.type == "oracle/MsgExchangeRateVote"
        assert MsgExchangeRateVote.action == "exchangeratevote"

    @given(other=st.text())
    def test_constructor_validates_addresses(self, acc_address, val_address, other):
        """MsgExchangeRateVote should validate `feeder` to be AccAddress and `validator`
        to be ValAddress.
        """
        assume(not is_val_address(other) and not is_acc_address(other))
        with pytest.raises(InvalidAccAddress):
            MsgExchangeRateVote(
                exchange_rate=Coin("ukrw", 1000),
                salt="",
                denom="ukrw",
                feeder=other,
                validator=val_address,
            )
        with pytest.raises(InvalidValAddress):
            MsgExchangeRateVote(
                exchange_rate=Coin("ukrw", 1000),
                salt="",
                denom="ukrw",
                feeder=acc_address,
                validator=other,
            )
        A = MsgExchangeRateVote(
            exchange_rate=Coin("ukrw", 1000),
            salt="",
            denom="ukrw",
            feeder=acc_address,
            validator=val_address,
        )
        assert A.feeder == acc_address
        assert A.validator == val_address

    @pytest.mark.parametrize("t", [int, Dec, Decimal, str, lambda x: Coin("ukrw", x)])
    def test_constructor_canonizes_exchange_rate_to_coin(
        self, acc_address, val_address, t
    ):
        A = MsgExchangeRateVote(
            exchange_rate=t(1000),
            salt="",
            denom="ukrw",
            feeder=acc_address,
            validator=val_address,
        )

        assert isinstance(A.exchange_rate, Coin)
        assert A.exchange_rate.denom == "ukrw"

    def test_exchange_rate_wrong_denom(self, acc_address, val_address):
        """Passing in `exchange_rate` as `Coin` will require both the `Coin.denom` and `denom`
        parameter to match.
        """

        with pytest.raises(ValidationError):
            MsgExchangeRateVote(
                exchange_rate=Coin("ukrw", 1000),
                salt="",
                denom="uusd",
                feeder=acc_address,
                validator=val_address,
            )

        A = MsgExchangeRateVote(
            exchange_rate=Coin("ukrw", 1000),
            salt="",
            denom="ukrw",
            feeder=acc_address,
            validator=val_address,
        )

        assert A.exchange_rate.denom == A.denom

    def test_vote_hash(self):

        msg1 = MsgExchangeRateVote(
            exchange_rate=Coin("umnt", "603.899000000000000000"),
            salt="0dff",
            denom="umnt",
            feeder="terra13ld7qfuq37328mw6f5kunez3e2ygqumxfcysms",
            validator="terravaloper1vqnhgc6d0jyggtytzqrnsc40r4zez6tx99382w",
        )

        assert msg1.vote_hash == "b338c8a65a132edcf3e9a13013997cdf1e2b283d"


class TestMsgExchangeRatePrevote:
    def test_schema_valid(self, msg_examples):
        for m in msg_examples[MsgExchangeRatePrevote]:
            assert_serdes_consistent(MsgExchangeRatePrevote, m)
            assert_serdes_exact(MsgExchangeRatePrevote, m)

    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(MsgExchangeRatePrevote.__schema__))
    def test_serdes_consistent(self, m):
        assert_serdes_consistent(MsgExchangeRatePrevote, m)

    def test_matches_meta(self):
        assert MsgExchangeRatePrevote.type == "oracle/MsgExchangeRatePrevote"
        assert MsgExchangeRatePrevote.action == "exchangerateprevote"

    @given(other=st.text())
    def test_constructor_validates_addresses(self, acc_address, val_address, other):
        """`MsgExchangeRateVote` should validate `feeder` to be AccAddress and `validator`
        to be ValAddress.
        """
        assume(not is_val_address(other) and not is_acc_address(other))
        with pytest.raises(InvalidAccAddress):
            MsgExchangeRatePrevote(
                hash="", denom="", feeder=other, validator=val_address,
            )
        with pytest.raises(InvalidValAddress):
            MsgExchangeRatePrevote(
                hash="", denom="", feeder=acc_address, validator=other,
            )
        A = MsgExchangeRatePrevote(
            hash="", denom="", feeder=acc_address, validator=val_address,
        )
        assert A.feeder == acc_address
        assert A.validator == val_address


class TestMsgDelegateFeedConsent:
    def test_schema_valid(self, msg_examples):
        for m in msg_examples[MsgDelegateFeedConsent]:
            assert_serdes_consistent(MsgDelegateFeedConsent, m)
            assert_serdes_exact(MsgDelegateFeedConsent, m)

    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(MsgDelegateFeedConsent.__schema__))
    def test_schema(self, m):
        assert_serdes_consistent(MsgDelegateFeedConsent, m)

    def test_matches_meta(self):
        assert MsgDelegateFeedConsent.type == "oracle/MsgDelegateFeedConsent"
        assert MsgDelegateFeedConsent.action == "delegatefeeder"

    @given(other=st.text())
    def test_constructor_validates_addresses(self, acc_address, val_address, other):
        """MsgDelegateFeedConsent should validate `operator` to be ValAddress and `delegate`
        to be AccAddress.
        """
        assume(not is_val_address(other) and not is_acc_address(other))
        with pytest.raises(InvalidValAddress):
            MsgDelegateFeedConsent(operator=other, delegate=acc_address)
        with pytest.raises(InvalidAccAddress):
            MsgDelegateFeedConsent(operator=val_address, delegate=other)
        A = MsgDelegateFeedConsent(operator=val_address, delegate=acc_address)
        assert A.operator == val_address
        assert A.delegate == acc_address
