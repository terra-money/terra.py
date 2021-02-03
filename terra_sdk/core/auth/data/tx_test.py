from terra_sdk.core.auth import StdTx


def test_deserializes_stdtx(load_json_examples):
    data = load_json_examples("./StdTx.data.json")
    for example in data["txs"]:
        parsed = StdTx.from_data(example["tx"]).to_data()["value"]
        for key in parsed.keys():
            assert parsed[key] == example["tx"]["value"][key]
