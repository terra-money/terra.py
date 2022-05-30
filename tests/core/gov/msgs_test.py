from terra_sdk.core.gov import MsgDeposit, MsgSubmitProposal


def test_deserializes_msg_deposit_examples(load_msg_examples):
    examples = load_msg_examples(MsgDeposit.type_amino, "./MsgDeposit.data.json")
    for example in examples:
        target = MsgDeposit.from_data(example["value"]).to_data()

        assert target["depositor"] == example["value"]["depositor"]
        assert target["proposal_id"] == example["value"]["proposal_id"]
        assert target["amount"] == example["value"]["amount"]
