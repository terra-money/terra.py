from terra_sdk.core.auth import Account, LazyGradedVestingAccount


def test_deserializes_account_example(load_json_examples):
    examples = load_json_examples("./Account.data.json")
    for example in examples:
        assert Account.from_data(example).to_data() == example


def test_deserializes_lazy_graded_vesting_account_example(load_json_examples):
    examples = load_json_examples("./LazyGradedVestingAccount.data.json")
    for example in examples:
        assert LazyGradedVestingAccount.from_data(example).to_data() == example
