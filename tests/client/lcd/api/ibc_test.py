from terra_sdk.client.lcd import LCDClient

terra = LCDClient(
    url="https://bombay-lcd.terra.dev/",
    chain_id="bombay-12",
)


def test_parameters():
    result = terra.ibc.parameters()
    assert result.get("allowed_clients")
