from terra_sdk.core.staking import Validator


def test_deserializes():
    validator_data = {
        "operator_address": "terravaloper1ptyzewnns2kn37ewtmv6ppsvhdnmeapvgk6d65",
        "consensus_pubkey": "terravalconspub1zcjduepqtcng29gnnhs8sv6dvv7cc0szyg3mu3tzzzjsw5x3x6pwgd2uqkkqes8fs5",
        "jailed": False,
        "status": 2,
        "tokens": "111401100001",
        "delegator_shares": "111401100001.000000000000000000",
        "description": {
            "moniker": "WeStaking",
            "identity": "DA9C5AD3E308E426",
            "website": "https://www.westaking.io",
            "details": "Delegate your luna to us for the staking rewards. We will do our best as secure and stable validator.",
        },
        "unbonding_height": "0",
        "unbonding_time": "1970-01-01T00:00:00Z",
        "commission": {
            "commission_rates": {
                "rate": "0.200000000000000000",
                "max_rate": "0.250000000000000000",
                "max_change_rate": "0.010000000000000000",
            },
            "update_time": "2019-12-01T03:28:34.024363013Z",
        },
        "min_self_delegation": "1",
    }

    validator = Validator.from_data(validator_data)

    assert validator_data == validator.to_data()
