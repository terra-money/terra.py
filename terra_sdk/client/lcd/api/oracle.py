from ._base import BaseAPI

from typing import Optional, List

from terra_sdk.core import Coin, AccAddress
from terra_sdk.core.oracle import (
    ExchangeRatePrevote,
    ExchangeRateVote,
    AggregateExchangeRatePrevote,
    AggregateExchangeRateVote,
)


class OracleAPI(BaseAPI):
    async def votes(
        self, denom: Optional[str] = None, validator: Optional[str] = None
    ) -> ExchangeRateVote:
        if denom is not None and validator is not None:
            res = self._c._get(f"/oracle/denoms/{denom}/votes/{validator}")
            return [ExchangeRateVote.from_data(res)]
        elif validator is not None:
            res = self._c._get(f"/oracle/voters/{validator}/votes")
            return list(map(ExchangeRateVote.from_data, res))
        elif denom is not None:
            res = self._c._get(f"/oracle/denoms/{denom}/votes")
            return list(map(ExchangeRateVote.from_data, res))
        else:
            raise TypeError("both denom and validator cannot both be None")

    async def exchange_rates(self) -> Coins:
        res = self._c._get(f"/oracle/denoms/exchange_rates", raw=True)
        if res.get("result"):
            return Coins.from_data(res)
        else:
            return Coins({})

    async def exchange_rate(self, denom: str) -> Coin:
        rates = await self.exchange_rates
        return rates.get(denom)

    async def active_denoms(self) -> List[str]:
        return await self._c._get(f"/oracle/denoms/exchange_rates")

    async def feeder_address(self) -> AccAddress:
        return await self._c._get(f"/oracle/voters/{validator}/feeder")

    async def misses(self, validator: str) -> int:
        return int(await self._c._get(f"/oracle/voters/{validator}/miss"))

    async def aggregate_prevote(self, validator: str) -> AggregateExchangeRatePrevote:
        res = await self._c._get(f"/oracle/voters/{validator}/aggregate_prevote")
        return AggregateExchangeRatePrevote.from_data(res)

    async def aggregate_vote(self, validator: str) -> AggregateExchangeRateVote:
        res = await self._c._get(f"/oracle/voters/{validator}/aggregate_vote")
        return AggregateExchangeRateVote.from_data(res)

    async def parameters(self) -> dict:
        return await self._c._get(f"/oracle/parameters")
