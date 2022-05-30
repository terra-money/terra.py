from terra_sdk.client.lcd import LCDClient

terra = LCDClient(
    chain_id="pisco-1",
    url="https://pisco-lcd.terra.dev/",
)
res = terra.tendermint.node_info()
print(res)
