from terra_sdk.core.auth import BaseAccount, DelayedVestingAccount, ContinuousVestingAccount, PeriodicVestingAccount


def test_deserializes_account_example(load_json_examples):
    examples = load_json_examples("./Account.data.json")
    for example in examples:
        target = BaseAccount.from_amino(example).to_amino()
        assert target["type"] == example["type"]
        assert target["value"]== example["value"]

def test_deserializes_continuous_vesting_account_example(load_json_examples):
    examples = load_json_examples("./ContinuousVestingAccount.data.json")
    for example in examples:
        target = ContinuousVestingAccount.from_amino(example).to_amino()
        assert target["type"] == example["type"]
        assert target["value"]["start_time"] == example["value"]["start_time"]


def test_deserializes_delayed_vesting_account_example(load_json_examples):
    examples = load_json_examples("./DelayedVestingAccount.data.json")
    for example in examples:
        target = DelayedVestingAccount.from_amino(example).to_amino()
        assert target["type"] == example["type"]


def test_deserializes_periodic_vesting_account_example(load_json_examples):
    examples = load_json_examples("./PeriodicVestingAccount.data.json")
    for example in examples:
        target = PeriodicVestingAccount.from_amino(example).to_amino()
        assert target["type"] == example["type"]
        assert target["value"]["start_time"] == example["value"]["start_time"]
        assert target["value"]["vesting_periods"] == example["value"]["vesting_periods"]