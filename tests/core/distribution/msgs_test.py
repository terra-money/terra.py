from terra_sdk.core.distribution import (
    MsgSetWithdrawAddress,
    MsgWithdrawDelegatorReward,
    MsgWithdrawValidatorCommission,
)


def test_deserializes_msg_modify_withdraw_address_examples(load_msg_examples):
    examples = load_msg_examples(
        MsgSetWithdrawAddress.type_amino, "./MsgModifyWithdrawAddress.data.json"
    )
    for example in examples:
        target = MsgSetWithdrawAddress.from_data(example["value"]).to_data()

        assert target["delegator_address"] == example["value"]["delegator_address"]
        assert target["withdraw_address"] == example["value"]["withdraw_address"]


def test_deserializes_msg_withdraw_delegation_reward_examples(load_msg_examples):
    examples = load_msg_examples(
        MsgWithdrawDelegatorReward.type_amino, "./MsgWithdrawDelegationReward.data.json"
    )
    for example in examples:
        target = MsgWithdrawDelegatorReward.from_data(example["value"]).to_data()

        assert target["delegator_address"] == example["value"]["delegator_address"]
        assert target["validator_address"] == example["value"]["validator_address"]


def test_deserializes_msg_withdraw_validator_commission_examples(load_msg_examples):
    examples = load_msg_examples(
        MsgWithdrawValidatorCommission.type_amino,
        "./MsgWithdrawValidatorCommission.data.json",
    )
    for example in examples:
        target = MsgWithdrawValidatorCommission.from_data(example["value"]).to_data()

        assert target["validator_address"] == example["value"]["validator_address"]
