from terra_sdk.client.lcd import LCDClient

bombay = LCDClient(url="https://bombay-lcd.terra.dev", chain_id="bombay-0001")

parameters = bombay.market.parameters()
assert "pool_recovery_period" in parameters
assert "mint_base_pool" in parameters
assert "burn_base_pool" in parameters
assert "min_stability_spread" in parameters
