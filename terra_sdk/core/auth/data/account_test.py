from terra_sdk.core.auth import Account


def test_deserializes_example(load_json_examples):
    examples = load_json_examples(__file__, "./Account.data.json")
    for example in examples:
        assert Account.from_data(example).to_data() == example