from terra_sdk.client.lcd import LCDClient
from terra_sdk.core import Coin, Coins, Dec

bombay = LCDClient(url="https://bombay-lcd.terra.dev", chain_id="bombay-0001")

parameters = bombay.treasury.parameters()
assert "tax_policy" in parameters
assert "reward_policy" in parameters
assert "seigniorage_burden_target" in parameters
assert "mining_increment" in parameters
assert "window_short" in parameters
assert "window_long" in parameters
assert "window_probation" in parameters

tax_cap = bombay.treasury.tax_cap("uluna")
assert type(tax_cap) == Coin

tax_rate = bombay.treasury.tax_rate()
assert type(tax_rate) == Dec

reward_weight = bombay.treasury.reward_weight()
assert type(reward_weight) == Dec

tax_proceeds = bombay.treasury.tax_proceeds()
assert type(tax_proceeds) == Coins

seigniorage_proceeds = bombay.treasury.seigniorage_proceeds()
assert type(seigniorage_proceeds) == Coin
