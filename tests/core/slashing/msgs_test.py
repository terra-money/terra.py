from terra_sdk.core.slashing.msgs import MsgUnjail


def test_deserializes_msg_unjail_examples(load_msg_examples):
    examples = load_msg_examples(MsgUnjail.type_amino, "./MsgUnjail.data.json")
    for example in examples:
        target = MsgUnjail.from_data(example["value"]).to_data()

        assert target["address"] == example["value"]["address"]
