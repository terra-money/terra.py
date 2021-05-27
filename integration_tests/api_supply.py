from terra_sdk.client.lcd import LCDClient
from terra_sdk.core import Coins

bombay = LCDClient(url="https://bombay-lcd.terra.dev", chain_id="bombay-0001")

total_supply = bombay.supply.total()
assert type(total_supply) == Coins
