from terra_sdk.core.staking import UnbondingDelegation, Delegation, Redelegation


def test_deserialize_unbonding_delegation_examples(load_json_examples):
    examples = load_json_examples(__file__, "./UnbondingDelegation.data.json")
    for example in examples:
        assert UnbondingDelegation.from_data(example).to_data() == example


def test_deserialize_delegation_examples(load_json_examples):
    examples = load_json_examples(__file__, "./Delegation.data.json")
    for example in examples:
        assert Delegation.from_data(example).to_data() == example


def test_deserialize_redelegation_examples(load_json_examples):
    examples = load_json_examples(__file__, "./Redelegation.data.json")
    for example in examples:
        assert Redelegation.from_data(example).to_data() == example
