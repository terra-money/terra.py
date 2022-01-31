from terra_sdk.client.lcd import LCDClient
from terra_sdk.util.contract import get_contract_events

bombay = LCDClient(url="https://lcd.terra.dev", chain_id="columbus-5")
tx_info = bombay.tx.tx_info(
    "D1E80F27435215FF097141C804EDE51C87718355CA8A6A397CC2346144F19D04"
)
print(get_contract_events(tx_info))
