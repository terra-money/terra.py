from terra_sdk.client.lcd import LCDClient

terra = LCDClient(
    url="https://pisco-lcd.terra.dev/",
    chain_id="pisco-1",
)


def test_parameters():
    result = terra.ibc.parameters()
    assert result.get("allowed_clients")
