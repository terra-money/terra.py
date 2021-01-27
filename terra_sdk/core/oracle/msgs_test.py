from terra_sdk.core.oracle import (
    MsgExchangeRatePrevote,
    MsgExchangeRateVote,
    MsgDelegateFeedConsent,
    # MsgAggregateExchangeRatePrevote, TODO
    # MsgAggregateExchangeRateVote,
)


def test_deserializes_msg_exchange_rate_prevote_examples(load_msg_examples):
    examples = load_msg_examples(
        MsgExchangeRatePrevote.type, "./MsgExchangeRatePrevote.data.json"
    )
    for example in examples:
        assert MsgExchangeRatePrevote.from_data(example).to_data() == example


def test_deserializes_msg_exchange_rate_vote_examples(load_msg_examples):
    examples = load_msg_examples(
        MsgExchangeRateVote.type, "./MsgExchangeRateVote.data.json"
    )
    for example in examples:
        assert MsgExchangeRateVote.from_data(example).to_data() == example


def test_deserializes_msg_delegate_feed_consent_examples(load_msg_examples):
    examples = load_msg_examples(
        MsgDelegateFeedConsent.type, "./MsgDelegateFeedConsent.data.json"
    )
    for example in examples:
        assert MsgDelegateFeedConsent.from_data(example).to_data() == example


# def test_deserializes_msg_aggregate_exchange_rate_prevote_examples(load_msg_examples):
#     examples = load_msg_examples(
#         MsgAggregateExchangeRatePrevote.type, "./MsgAggregateExchangePrevote.data.json"
#     )
#     for example in examples:
#         assert MsgAggregateExchangeRatePrevote.from_data(example).to_data() == example


# def test_deserializes_msg_aggregate_exchange_rate_vote_examples(load_msg_examples):
#     examples = load_msg_examples(
#         MsgAggregateExchangeRateVote.type, "./MsgAggregateExchangeVote.data.json"
#     )
#     for example in examples:
#         assert MsgAggregateExchangeRateVote.from_data(example).to_data() == example
