from terra_sdk.core.auth import Account, DelayedVestingAccount, ContinuousVestingAccount, PeriodicVestingAccount


def test_deserializes_account_example(load_json_examples):
    examples = load_json_examples("./Account.data.json")
    for example in examples:
        assert Account.from_amino(example).to_amino() == example

def test_deserializes_continuous_vesting_account_example(load_json_examples):
    examples = load_json_examples("./ContinuousVestingAccount.data.json")
    for example in examples:
        assert ContinuousVestingAccount.from_amino(example).to_amino() == example

def test_deserializes_delayed_vesting_account_example(load_json_examples):
    examples = load_json_examples("./DelayedVestingAccount.data.json")
    for example in examples:
        assert DelayedVestingAccount.from_amino(example).to_amino() == example

def test_deserializes_periodic_vesting_account_example(load_json_examples):
    examples = load_json_examples("./PeriodicVestingAccount.data.json")
    for example in examples:
        assert PeriodicVestingAccount.from_amino(example).to_amino() == example
