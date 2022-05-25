from terra_sdk.client.lcd import LCDClient
from terra_sdk.core.bech32 import is_acc_address

terra = LCDClient(
    url="https://pisco-lcd.terra.dev/",
    chain_id="pisco-1",
)

def test_rewards():
    result = terra.distribution.rewards("terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v")
    assert result.total.to_data()


def test_validator_commission():
    result = terra.distribution.validator_commission(
        "terravaloper19ne0aqltndwxl0n32zyuglp2z8mm3nu0gxpfaw"
    )
    assert result.to_data()


def test_withdraw_address():
    result = terra.distribution.withdraw_address(
        "terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v"
    )
    assert is_acc_address(result)


def test_comminity_pool():
    result = terra.distribution.community_pool()
    assert result.to_data()


def test_parameters():
    result = terra.distribution.parameters()
    assert result.get("community_tax")
    assert result.get("base_proposer_reward")
    assert result.get("bonus_proposer_reward")
    assert result.get("withdraw_addr_enabled")
