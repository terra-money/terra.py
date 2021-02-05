from terra_sdk.core.distribution import (
    MsgModifyWithdrawAddress,
    MsgWithdrawDelegationReward,
    MsgWithdrawValidatorCommission,
)


def test_deserializes_msg_modify_withdraw_address_examples(load_msg_examples):
    examples = load_msg_examples(
        MsgModifyWithdrawAddress.type, "./MsgModifyWithdrawAddress.data.json"
    )
    for example in examples:
        assert MsgModifyWithdrawAddress.from_data(example).to_data() == example


def test_deserializes_msg_withdraw_delegation_reward_examples(load_msg_examples):
    examples = load_msg_examples(
        MsgWithdrawDelegationReward.type, "./MsgWithdrawDelegationReward.data.json"
    )
    for example in examples:
        assert MsgWithdrawDelegationReward.from_data(example).to_data() == example


def test_deserializes_msg_withdraw_validator_commission_examples(load_msg_examples):
    examples = load_msg_examples(
        MsgWithdrawValidatorCommission.type,
        "./MsgWithdrawValidatorCommission.data.json",
    )
    for example in examples:
        assert MsgWithdrawValidatorCommission.from_data(example).to_data() == example
