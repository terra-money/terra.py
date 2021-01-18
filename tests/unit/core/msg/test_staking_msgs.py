import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st
from hypothesis_jsonschema import from_schema

from terra_sdk.core.msg.staking import (
    MsgBeginRedelegate,
    MsgCreateValidator,
    MsgDelegate,
    MsgEditValidator,
    MsgUndelegate,
)
from terra_sdk.error import InvalidAccAddress, InvalidValAddress
from terra_sdk.util.validation import is_acc_address, is_val_address
from testtools import assert_serdes_consistent, assert_serdes_exact, load_msg_examples


@pytest.fixture(scope="module")
def msg_examples(tdd):
    """Stores the __schema__ validation set for staking messages."""
    return load_msg_examples(
        tdd,
        msg_types=[
            MsgBeginRedelegate,
            MsgCreateValidator,
            MsgDelegate,
            MsgEditValidator,
            MsgUndelegate,
        ],
    )


class TestMsgBeginRedelegate:
    def test_schema_valid(self, msg_examples):
        for m in msg_examples[MsgBeginRedelegate]:
            assert_serdes_consistent(MsgBeginRedelegate, m)
            assert_serdes_exact(MsgBeginRedelegate, m)

    @pytest.mark.serdes
    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(MsgBeginRedelegate.__schema__))
    def test_serdes_consistent(self, m):
        assert_serdes_consistent(MsgBeginRedelegate, m)

    def test_matches_meta(self):
        assert MsgBeginRedelegate.type == "staking/MsgBeginRedelegate"
        assert MsgBeginRedelegate.action == "begin_redelegate"

    @given(other=st.text())
    def test_constructor_validates_addresses(self, acc_address, val_address, other):
        """MsgBeginRedelegate should validate `delegator` to be AccAddress, and both
        `validator_src_address` and `validator_dst_address` to be ValAddress.
        """
        assume(not is_acc_address(other) and not is_val_address(other))
        with pytest.raises(InvalidAccAddress):
            MsgBeginRedelegate(
                delegator_address=other,
                validator_src_address=val_address,
                validator_dst_address=val_address,
                amount=None,
            )
        with pytest.raises(InvalidValAddress):
            MsgBeginRedelegate(
                delegator_address=acc_address,
                validator_src_address=other,
                validator_dst_address=val_address,
                amount=None,
            )
        with pytest.raises(InvalidValAddress):
            MsgBeginRedelegate(
                delegator_address=acc_address,
                validator_src_address=val_address,
                validator_dst_address=other,
                amount=None,
            )
        A = MsgBeginRedelegate(
            delegator_address=acc_address,
            validator_src_address=val_address,
            validator_dst_address=val_address,
            amount=None,
        )
        assert A.delegator_address == acc_address
        assert A.validator_src_address == val_address
        assert A.validator_dst_address == val_address


class TestMsgCreateValidator:
    def test_schema_valid(self, msg_examples):
        for m in msg_examples[MsgCreateValidator]:
            assert_serdes_consistent(MsgCreateValidator, m)
            assert_serdes_exact(MsgCreateValidator, m)

    @pytest.mark.serdes
    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(MsgCreateValidator.__schema__))
    def test_serdes_consistent(self, m):
        assert_serdes_consistent(MsgCreateValidator, m)

    def test_matches_meta(self):
        assert MsgCreateValidator.type == "staking/MsgCreateValidator"
        assert MsgCreateValidator.action == "create_validator"


class TestMsgDelegate:
    def test_schema_valid(self, msg_examples):
        for m in msg_examples[MsgDelegate]:
            assert_serdes_consistent(MsgDelegate, m)
            assert_serdes_exact(MsgDelegate, m)

    @pytest.mark.serdes
    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(MsgDelegate.schema))
    def test_serdes_consistent(self, m):
        assert_serdes_consistent(MsgDelegate, m)

    def test_matches_meta(self):
        assert MsgDelegate.type == "staking/MsgDelegate"
        assert MsgDelegate.action == "delegate"


class TestMsgEditValidator:
    def test_schema_valid(self, msg_examples):
        for m in msg_examples[MsgEditValidator]:
            assert_serdes_consistent(MsgEditValidator, m)
            assert_serdes_exact(MsgEditValidator, m)

    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(MsgEditValidator.__schema__))
    def test_serdes_consistent(self, m):
        assert_serdes_consistent(MsgEditValidator, m)

    def test_matches_meta(self):
        assert MsgEditValidator.type == "staking/MsgEditValidator"
        assert MsgEditValidator.action == "edit_validator"


class TestMsgUndelegate:
    def test_schema_valid(self, msg_examples):
        for m in msg_examples[MsgUndelegate]:
            assert_serdes_consistent(MsgUndelegate, m)
            assert_serdes_exact(MsgUndelegate, m)

    @pytest.mark.serdes
    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(MsgUndelegate.__schema__))
    def test_schema(self, m):
        assert_serdes_consistent(MsgUndelegate, m)

    def test_matches_meta(self):
        assert MsgUndelegate.type == "staking/MsgUndelegate"
        assert MsgUndelegate.action == "begin_unbonding"
