from terra_sdk.client.lcd import LCDClient

bombay = LCDClient(url="https://bombay-lcd.terra.dev", chain_id="bombay-0001")

parameters = bombay.treasury.parameters()
assert "tax_policy" in parameters
assert "reward_policy" in parameters
assert "seigniorage_burden_target" in parameters
assert "mining_increment" in parameters
assert "window_short" in parameters
assert "window_long" in parameters
assert "window_probation" in parameters
