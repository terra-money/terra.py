from terra_sdk.core.gov import MsgDeposit, MsgSubmitProposal


def test_deserializes_msg_deposit_examples(load_msg_examples):
    examples = load_msg_examples(MsgDeposit.type, "./MsgDeposit.data.json")
    for example in examples:
        assert MsgDeposit.from_data(example).to_data() == example


def test_deserializes_msg_submit_proposal_examples(load_msg_examples):
    examples = load_msg_examples(
        MsgSubmitProposal.type, "./MsgSubmitProposal.data.json"
    )
    for example in examples:
        assert MsgSubmitProposal.from_data(example).to_data() == example
