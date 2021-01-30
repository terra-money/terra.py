from terra_sdk.core.market import MsgSwap, MsgSwapSend


def test_deserializes_msg_swap_examples(load_msg_examples):
    examples = load_msg_examples(MsgSwap.type, "./MsgSwap.data.json")
    for example in examples:
        assert MsgSwap.from_data(example).to_data() == example


def test_deserializes_msg_swap_send_examples(load_msg_examples):
    examples = load_msg_examples(MsgSwapSend.type, "./MsgSwapSend.data.json")
    for example in examples:
        assert MsgSwapSend.from_data(example).to_data() == example
