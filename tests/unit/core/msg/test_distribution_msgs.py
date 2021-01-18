import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st
from hypothesis_jsonschema import from_schema

from terra_sdk.core.msg.distribution import (
    MsgModifyWithdrawAddress,
    MsgWithdrawDelegationReward,
    MsgWithdrawValidatorCommission,
)
from terra_sdk.util.validation import (
    InvalidAccAddress,
    InvalidValAddress,
    is_acc_address,
    is_val_address,
)
from testtools import assert_serdes_consistent, assert_serdes_exact, load_msg_examples


@pytest.fixture(scope="module")
def msg_examples(tdd):
    """Stores the __schema__ validation set for distribution messages."""
    return load_msg_examples(
        tdd,
        msg_types=[
            MsgModifyWithdrawAddress,
            MsgWithdrawDelegationReward,
            MsgWithdrawValidatorCommission,
        ],
    )


class TestMsgModifyWithdrawAddress:
    def test_schema_valid(self, msg_examples):
        for m in msg_examples[MsgModifyWithdrawAddress]:
            assert_serdes_consistent(MsgModifyWithdrawAddress, m)
            assert_serdes_exact(MsgModifyWithdrawAddress, m)

    @pytest.mark.serdes
    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(MsgModifyWithdrawAddress.__schema__))
    def test_serdes_consistent(self, m):
        assert_serdes_consistent(MsgModifyWithdrawAddress, m)

    def test_matches_meta(self):
        assert MsgModifyWithdrawAddress.type == "distribution/MsgModifyWithdrawAddress"
        assert MsgModifyWithdrawAddress.action == "set_withdraw_address"

    @given(other=st.text())
    def test_constructor_validates_addresses(self, acc_address, other):
        """MsgModifyWithdrawAddress should validate `delegator_address` and `withdraw_address` to
        be correct AccAddress.
        """

        assume(not is_acc_address(other))
        with pytest.raises(InvalidAccAddress):
            MsgModifyWithdrawAddress(
                delegator_address=other, withdraw_address=acc_address
            )
        with pytest.raises(InvalidAccAddress):
            MsgModifyWithdrawAddress(
                delegator_address=acc_address, withdraw_address=other
            )
        A = MsgModifyWithdrawAddress(
            delegator_address=acc_address, withdraw_address=acc_address
        )
        assert A.delegator_address == acc_address


class TestMsgWithdrawDelegationReward:
    def test_schema_valid(self, msg_examples):
        for m in msg_examples[MsgWithdrawDelegationReward]:
            assert_serdes_consistent(MsgWithdrawDelegationReward, m)
            assert_serdes_exact(MsgWithdrawDelegationReward, m)

    @pytest.mark.serdes
    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(MsgWithdrawDelegationReward.schema))
    def test_serdes_consistent(self, m):
        assert_serdes_consistent(MsgWithdrawDelegationReward, m)

    def test_matches_meta(self):
        assert (
            MsgWithdrawDelegationReward.type
            == "distribution/MsgWithdrawDelegationReward"
        )
        assert MsgWithdrawDelegationReward.action == "withdraw_delegation_reward"

    @given(other=st.text())
    def test_constructor_validates_addresses(self, acc_address, val_address, other):
        """MsgWithdrawDelegationReward should validate `delegator_address` to be AccAddress
        and `withdraw_address` to be ValAddress.
        """

        assume(not is_acc_address(other) and not is_val_address(other))
        with pytest.raises(InvalidAccAddress):
            MsgWithdrawDelegationReward(
                delegator_address=other, validator_address=val_address
            )
        with pytest.raises(InvalidValAddress):
            MsgWithdrawDelegationReward(
                delegator_address=acc_address, validator_address=other
            )
        A = MsgWithdrawDelegationReward(
            delegator_address=acc_address, validator_address=val_address
        )
        assert A.delegator_address == acc_address
        assert A.validator_address == val_address


class TestMsgWithdrawValidatorCommission:
    def test_schema_valid(self, msg_examples):
        for m in msg_examples[MsgWithdrawValidatorCommission]:
            assert_serdes_consistent(MsgWithdrawValidatorCommission, m)
            assert_serdes_exact(MsgWithdrawValidatorCommission, m)

    @pytest.mark.serdes
    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(MsgWithdrawValidatorCommission.__schema__))
    def test_serdes_consistent(self, m):
        assert_serdes_consistent(MsgWithdrawValidatorCommission, m)

    def test_matches_meta(self):
        assert (
            MsgWithdrawValidatorCommission.type
            == "distribution/MsgWithdrawValidatorCommission"
        )
        assert MsgWithdrawValidatorCommission.action == "withdraw_validator_commission"

    @given(other=st.text())
    def test_constructor_validates_addresses(self, val_address, other):
        """MsgWithdrawValidatorCommission should validate `validator_address` to be ValAddress.
        """

        assume(not is_val_address(other))
        with pytest.raises(InvalidValAddress):
            MsgWithdrawValidatorCommission(validator_address=other)
        A = MsgWithdrawValidatorCommission(validator_address=val_address)
        assert A.validator_address == val_address
