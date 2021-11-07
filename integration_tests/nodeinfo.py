from terra_sdk.client.lcd import LCDClient

terra = LCDClient(
    chain_id="bombay-12",
    url="https://bombay-lcd.terra.dev/",
)
res = terra.tendermint.node_info()
print(res)
