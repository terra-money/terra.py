from terra_sdk.client.lcd import LCDClient
from terra_sdk.core import Coin, Dec

bombay = LCDClient(url="https://bombay-lcd.terra.dev", chain_id="bombay-0001")

parameters = bombay.market.parameters()
assert "pool_recovery_period" in parameters
assert "mint_base_pool" in parameters
assert "burn_base_pool" in parameters
assert "min_stability_spread" in parameters

offer_coin = Coin("uluna", 1)
ask_denom = "uusd"

swap_rate = bombay.market.swap_rate(offer_coin, ask_denom)
assert type(swap_rate) == Coin

mint_pool_delta = bombay.market.mint_pool_delta()
assert type(mint_pool_delta) == Dec

burn_pool_delta = bombay.market.burn_pool_delta()
assert type(burn_pool_delta) == Dec
