from terra_sdk.client.lcd import LCDClient

terra = LCDClient(chain_id="columbus-4", url="https://lcd.terra.dev")
node_info = terra.tendermint.node_info()
print(terra.tendermint.node_info.__doc__)
