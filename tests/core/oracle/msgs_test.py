from terra_sdk.core.oracle import MsgAggregateExchangeRateVote, MsgDelegateFeedConsent


def test_deserializes_msg_delegate_feed_consent_examples(load_msg_examples):
    examples = load_msg_examples(
        MsgDelegateFeedConsent.type, "./MsgDelegateFeedConsent.data.json"
    )
    for example in examples:
        assert MsgDelegateFeedConsent.from_data(example).to_data() == example


def test_msg_aggregate_exchange_rate_vote_get_aggregate_vote_hash(load_msg_examples):
    msg = MsgAggregateExchangeRateVote(
        {
            "ukrw": "245.000",
            "uusd": "0.2242",
            "usdr": "0.182",
        },
        "salt",
        "terra1krj7amhhagjnyg2tkkuh6l0550y733jnjulzjh",
        "terravaloper1krj7amhhagjnyg2tkkuh6l0550y733jnjnnlzy",
    )

    assert (
        msg.get_aggregate_prevote().hash == "7929908433e7399845fa60f9ef70ef7f2bb8f01b"
    )
