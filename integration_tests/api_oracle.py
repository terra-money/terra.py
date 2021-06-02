from terra_sdk.client.lcd import LCDClient
from terra_sdk.core import AccAddress, Coin, Coins, ValAddress
from terra_sdk.core.oracle import (
    AggregateExchangeRatePrevote,
    AggregateExchangeRateVote,
    ExchangeRatePrevote,
    ExchangeRateVote,
)

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

exchange_rates = bombay.oracle.exchange_rates()
assert type(exchange_rates) == Coins

exchange_rate = bombay.oracle.exchange_rate('uusd')
assert type(exchange_rate) == Coin

active_denoms = bombay.oracle.active_denoms()
assert type(active_denoms[0]) == str if len(active_denoms) > 0 else True

validator_address = "terravaloper1qxqrtvg3smlfdfhvwcdzh0huh4f50kfs6gdt4x"

feeder_address = bombay.oracle.feeder_address(validator_address)
assert type(feeder_address) == AccAddress.__supertype__

misses = bombay.oracle.misses(validator_address)
assert type(misses) == int

aggregate_prevote = bombay.oracle.aggregate_prevote(validator_address)
assert type(aggregate_prevote) == AggregateExchangeRatePrevote if aggregate_prevote else True

aggregate_vote = bombay.oracle.aggregate_vote(validator_address)
assert type(aggregate_vote) == AggregateExchangeRateVote if aggregate_vote else True
