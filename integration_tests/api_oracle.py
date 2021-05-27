from terra_sdk.client.lcd import LCDClient

bombay = LCDClient(url="https://bombay-lcd.terra.dev", chain_id="bombay-0001")

parameters = bombay.oracle.parameters()
assert "vote_period" in parameters
assert "vote_threshold" in parameters
assert "reward_band" in parameters
assert "reward_distribution_window" in parameters
assert "whitelist" in parameters
assert "slash_fraction" in parameters
assert "slash_window" in parameters
assert "min_valid_per_window" in parameters
