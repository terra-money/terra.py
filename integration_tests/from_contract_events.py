from terra_sdk.client.lcd import LCDClient
from terra_sdk.util.contract import get_contract_events

bombay = LCDClient(url="https://bombay-lcd.terra.dev", chain_id="bombay-0001")
tx_info = bombay.tx.tx_info(
    "B652DF530D50E470070F3F211519495078082D01B49ED36B762B4E9446CE484E"
)
print(get_contract_events(tx_info))
