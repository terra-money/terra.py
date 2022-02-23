from terra_sdk.client.lcd import LCDClient
from terra_sdk.core import Coin

terra = LCDClient(
    url="https://bombay-lcd.terra.dev/",
    chain_id="bombay-12",
)


def test_swap_rate():
    result = terra.market.swap_rate(Coin.parse("10000uluna"), "uusd")
    assert (result is not None)


def test_pool_delta():
    result = terra.market.terra_pool_delta()
    assert (result is not None)


def test_parameters():
    result = terra.market.parameters()
    assert (result.get("base_pool"))
    assert (result.get("pool_recovery_period"))
    assert (result.get("min_stability_spread"))
