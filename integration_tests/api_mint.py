from terra_sdk.client.lcd import LCDClient
from terra_sdk.core import Dec

bombay = LCDClient(url="https://bombay-lcd.terra.dev", chain_id="bombay-0001")

inflation = bombay.mint.inflation()
assert type(inflation) == Dec

annual_provisions = bombay.mint.annual_provisions()
assert type(annual_provisions) == Dec

parameters = bombay.mint.parameters()
assert "mint_denom" in parameters
assert "inflation_rate_change" in parameters
assert "inflation_max" in parameters
assert "inflation_min" in parameters
assert "goal_bonded" in parameters
assert "blocks_per_year" in parameters
