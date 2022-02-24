from terra_sdk.core import Tx


def test_deserializes_tx(load_json_examples):
    data = load_json_examples("./StdTx.data.json")
    for example in data:
        parsed = Tx.from_amino(example).to_amino()["value"]
        for key in parsed.keys():
            assert parsed[key] == example["value"][key]
