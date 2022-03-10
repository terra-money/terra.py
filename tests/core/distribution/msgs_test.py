from terra_sdk.core.distribution import (
    MsgSetWithdrawAddress,
    MsgWithdrawDelegatorReward,
    MsgWithdrawValidatorCommission,
)


def test_deserializes_msg_modify_withdraw_address_examples(load_msg_examples):
    examples = load_msg_examples(
        MsgSetWithdrawAddress.type_url, "./MsgModifyWithdrawAddress.data.json"
    )
    for example in examples:
        assert MsgSetWithdrawAddress.from_data(example).to_data() == example


def test_deserializes_msg_withdraw_delegation_reward_examples(load_msg_examples):
    examples = load_msg_examples(
        MsgWithdrawDelegatorReward.type_url, "./MsgWithdrawDelegationReward.data.json"
    )
    for example in examples:
        assert MsgWithdrawDelegatorReward.from_data(example).to_data() == example


def test_deserializes_msg_withdraw_validator_commission_examples(load_msg_examples):
    examples = load_msg_examples(
        MsgWithdrawValidatorCommission.type_url,
        "./MsgWithdrawValidatorCommission.data.json",
    )
    for example in examples:
        assert MsgWithdrawValidatorCommission.from_data(example).to_data() == example
