from typing import List, Optional

from terra_sdk.core import AccAddress, Coin, Coins, Dec, Numeric, ValAddress
from terra_sdk.core.oracle import (
    AggregateExchangeRatePrevote,
    AggregateExchangeRateVote,
)
from terra_sdk.exceptions import LCDResponseError

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncOracleAPI", "OracleAPI"]


class AsyncOracleAPI(BaseAsyncAPI):
    async def exchange_rates(self) -> Coins:
        """Fetches registered exchange rates of Luna in all available denoms.

        Returns:
            Coins: exchange rates of Luna
        """
        res = await self._c._get("/terra/oracle/v1beta1/denoms/exchange_rates")
        rates = res.get("exchange_rates")
        if res:
            return Coins.from_data(rates)
        else:
            return Coins({})

    async def exchange_rate(self, denom: str) -> Coin:
        """Fetches registered exchange rate of Luna in a specific denom.

        Args:
            denom (str): denom

        Returns:
            Coin: exchange rate of Luna
        """
        res = await self._c._get(f"/terra/oracle/v1beta1/denoms/{denom}/exchange_rate")
        return Dec(res.get("exchange_rate"))

    async def active_denoms(self) -> List[str]:
        """Fetches current active denoms.

        Returns:
            List[str]: active denoms
        """
        res = await self._c._get("/terra/oracle/v1beta1/denoms/actives")
        return res.get("actives")

    async def feeder_address(self, validator: ValAddress) -> AccAddress:
        """Fetches associated feeder address for a validator.

        Args:
            validator (ValAddress): validator operator address

        Returns:
            AccAddress: feeder address
        """
        res = await self._c._get(f"/terra/oracle/v1beta1/validators/{validator}/feeder")
        return res.get("feeder_addr")

    async def misses(self, validator: ValAddress) -> int:
        """Fetches current value of miss counter for a validator.

        Args:
            validator (ValAddress): validator operator address

        Returns:
            int: current number of misses
        """
        res = await self._c._get(f"terra/oracle/v1beta1/validators/{validator}/miss")
        return int(res.get("miss_counter"))

    async def aggregate_prevote(
        self, validator: ValAddress
    ) -> Optional[AggregateExchangeRatePrevote]:
        """Fetches active aggregate prevote for a validator.

        Args:
            validator (ValAddress): validator operator address

        Returns:
            Optional[AggregateExchangeRatePrevote]: current aggegate prevote (if any).
        """
        try:
            res = await self._c._get(
                f"/terra/oracle/v1beta1/validators/{validator}/aggregate_prevote"
            )
        except LCDResponseError as e:
            if e.response.status == 404:
                return None
            else:
                raise e
        return AggregateExchangeRatePrevote.from_data(res.get("aggregate_prevote"))

    async def aggregate_vote(
        self, validator: ValAddress
    ) -> Optional[AggregateExchangeRateVote]:
        """Fetches active aggregate vote for a validator.

        Args:
            validator (ValAddress): validator operator address

        Returns:
            Optional[AggregateExchangeRatePrevote]: current aggegate vote (if any).
        """
        try:
            res = await self._c._get(
                f"/terra/oracle/v1beta1/validators/{validator}/aggregate_vote"
            )
        except LCDResponseError as e:
            if e.response.status == 404:
                return None
            else:
                raise e
        return AggregateExchangeRateVote.from_data(res.get("aggregate_vote"))

    async def parameters(self) -> dict:
        """Fetches Oracle module parameters.

        Returns:
            dict: Oracle module parameters
        """
        res = await self._c._get("/terra/oracle/v1beta1/params")
        params = res.get("params")
        return {
            "vote_period": Numeric.parse(params["vote_period"]),
            "vote_threshold": Dec(params["vote_threshold"]),
            "reward_band": Dec(params["reward_band"]),
            "reward_distribution_window": Numeric.parse(
                params["reward_distribution_window"]
            ),
            "whitelist": [
                {"name": x["name"], "tobin_tax": Dec(x["tobin_tax"])}
                for x in params["whitelist"]
            ],
            "slash_fraction": Dec(params["slash_fraction"]),
            "slash_window": Numeric.parse(params["slash_window"]),
            "min_valid_per_window": Dec(params["min_valid_per_window"]),
        }


class OracleAPI(AsyncOracleAPI):
    @sync_bind(AsyncOracleAPI.exchange_rates)
    def exchange_rates(self) -> Coins:
        pass

    exchange_rates.__doc__ = AsyncOracleAPI.exchange_rates.__doc__

    @sync_bind(AsyncOracleAPI.exchange_rate)
    def exchange_rate(self, denom: str) -> Coin:
        pass

    exchange_rate.__doc__ = AsyncOracleAPI.exchange_rate.__doc__

    @sync_bind(AsyncOracleAPI.active_denoms)
    def active_denoms(self) -> List[str]:
        pass

    active_denoms.__doc__ = AsyncOracleAPI.active_denoms.__doc__

    @sync_bind(AsyncOracleAPI.feeder_address)
    def feeder_address(self, validator: ValAddress) -> AccAddress:
        pass

    feeder_address.__doc__ = AsyncOracleAPI.active_denoms.__doc__

    @sync_bind(AsyncOracleAPI.misses)
    def misses(self, validator: ValAddress) -> int:
        pass

    misses.__doc__ = AsyncOracleAPI.misses.__doc__

    @sync_bind(AsyncOracleAPI.aggregate_prevote)
    def aggregate_prevote(
        self, validator: ValAddress
    ) -> Optional[AggregateExchangeRatePrevote]:
        pass

    aggregate_prevote.__doc__ = AsyncOracleAPI.aggregate_prevote.__doc__

    @sync_bind(AsyncOracleAPI.aggregate_vote)
    def aggregate_vote(
        self, validator: ValAddress
    ) -> Optional[AggregateExchangeRateVote]:
        pass

    aggregate_vote.__doc__ = AsyncOracleAPI.aggregate_vote.__doc__

    @sync_bind(AsyncOracleAPI.parameters)
    def parameters(self) -> dict:
        pass

    parameters.__doc__ = AsyncOracleAPI.parameters.__doc__
