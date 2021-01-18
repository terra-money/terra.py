from typing import List

from terra_sdk.core import Coin, ExchangeRatePrevote, ExchangeRateVote


class DenomQuery(object):
    def __init__(self, terra, denom: str):
        self.terra = terra
        self.denom = denom

    def __repr__(self):
        return f"DenomQuery({self.denom!r}) -> {self.terra}"

    def prevotes(self) -> List[ExchangeRatePrevote]:
        return self.terra.oracle.prevotes(denom=self.denom)

    def votes(self) -> List[ExchangeRateVote]:
        return self.terra.oracle.votes(denom=self.denom)

    def exchange_rate(self) -> Coin:
        return self.terra.oracle.exchange_rate(denom=self.denom)

    def supply(self) -> Coin:
        return self.terra.supply(denom=self.denom)

    def community_pool(self) -> Coin:
        return self.terra.distribution.community_pool(denom=self.denom)
