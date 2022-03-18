from terra_sdk.client.lcd import LCDClient
from terra_sdk.core.tx import Tx
terra = LCDClient(chain_id="columbus-5", url="https://lcd.terra.dev")
block = terra.tendermint.block_info()
tx = block['block']['data']['txs'][0]
tx = terra.tx.decode(tx)
terra.session.connector.limit=1
print(tx)