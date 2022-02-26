from terra_sdk.client.lcd import LCDClient

terra = LCDClient(
    url="https://bombay-lcd.terra.dev/",
    chain_id="bombay-12",
)


def test_parameters():
    result = terra.ibc_transfer.parameters()
    assert result.get("send_enabled")
    assert result.get("receive_enabled")
