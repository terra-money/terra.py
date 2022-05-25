from terra_sdk.client.lcd import LCDClient

terra = LCDClient(
    url="https://pisco-lcd.terra.dev/",
    chain_id="pisco-1",
)


def test_parameters():
    result = terra.ibc_transfer.parameters()
    assert result.get("send_enabled")
    assert result.get("receive_enabled")
