from terra_sdk.client.lcd import LCDClient

terra = LCDClient(
    url="https://pisco-lcd.terra.dev/",
    chain_id="pisco-1",
)


def test_validators_with_voting_power():
    validators_with_voting_power = terra.utils.validators_with_voting_power()
    print(validators_with_voting_power)
    assert validators_with_voting_power is not None
