from terra_sdk.core.staking import Delegation, Redelegation, UnbondingDelegation


def test_deserialize_unbonding_delegation_examples(load_json_examples):
    examples = load_json_examples("./UnbondingDelegation.data.json")
    for example in examples:
        assert UnbondingDelegation.from_data(example).to_data() == example


def test_deserialize_delegation_examples(load_json_examples):
    examples = load_json_examples("./Delegation.data.json")
    for example in examples:
        assert Delegation.from_data(example).to_data() == example


def test_deserialize_redelegation_examples(load_json_examples):
    examples = load_json_examples("./Redelegation.data.json")
    for example in examples:
        assert Redelegation.from_data(example).to_data() == example
