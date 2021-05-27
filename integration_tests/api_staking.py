from terra_sdk.client.lcd import LCDClient

bombay = LCDClient(url="https://bombay-lcd.terra.dev", chain_id="bombay-0001")

parameters = bombay.staking.parameters()
assert "unbonding_time" in parameters
assert "max_validators" in parameters
assert "max_entries" in parameters
assert "historical_entries" in parameters
assert "bond_denom" in parameters
assert "power_reduction" in parameters
