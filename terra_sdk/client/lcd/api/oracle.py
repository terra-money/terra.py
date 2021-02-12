from typing import List, Optional

from terra_sdk.core import AccAddress, Coin, Coins, ValAddress
from terra_sdk.core.oracle import (
    AggregateExchangeRatePrevote,
    AggregateExchangeRateVote,
    ExchangeRatePrevote,
    ExchangeRateVote,
)
from terra_sdk.exceptions import LCDResponseError

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncOracleAPI", "OracleAPI"]


class AsyncOracleAPI(BaseAsyncAPI):
    async def prevotes(
        self, denom: Optional[str] = None, validator: Optional[ValAddress] = None
    ) -> List[ExchangeRatePrevote]:
        """Fetches active oracle prevotes, filtering by denom, or validator, or both.

        Args:
            denom (Optional[str], optional): denom.
            validator (Optional[ValAddress], optional): validator operator address.

        Raises:
            TypeError: if both ``denom`` and ``validator`` are ``None``

        Returns:
            List[ExchangeRatePrevote]: prevotes
        """
        if denom is not None and validator is not None:
            res = await self._c._get(f"/oracle/denoms/{denom}/prevotes/{validator}")
            return [ExchangeRatePrevote.from_data(res)]
        elif validator is not None:
            res = await self._c._get(f"/oracle/voters/{validator}/prevotes")
            return [ExchangeRatePrevote.from_data(d) for d in res]
        elif denom is not None:
            res = await self._c._get(f"/oracle/denoms/{denom}/prevotes")
            return [ExchangeRatePrevote.from_data(d) for d in res]
        else:
            raise TypeError("both denom and validator cannot both be None")

    async def votes(
        self, denom: Optional[str] = None, validator: Optional[ValAddress] = None
    ) -> List[ExchangeRateVote]:
        """Fetches active oracle votes, filtering by denom, or validator, or both.

        Args:
            denom (Optional[str], optional): denom.
            validator (Optional[ValAddress], optional): validator operator address.

        Raises:
            TypeError: if both ``denom`` and ``validator`` are ``None``

        Returns:
            List[ExchangeRateVote]: votes
        """
        if denom is not None and validator is not None:
            res = await self._c._get(f"/oracle/denoms/{denom}/votes/{validator}")
            return [ExchangeRateVote.from_data(res)]
        elif validator is not None:
            res = await self._c._get(f"/oracle/voters/{validator}/votes")
            return [ExchangeRateVote.from_data(d) for d in res]
        elif denom is not None:
            res = await self._c._get(f"/oracle/denoms/{denom}/votes")
            return [ExchangeRateVote.from_data(d) for d in res]
        else:
            raise TypeError("both denom and validator cannot both be None")

    async def exchange_rates(self) -> Coins:
        """Fetches registered exchange rates of Luna in all available denoms.

        Returns:
            Coins: exchange rates of Luna
        """
        res = await self._c._get("/oracle/denoms/exchange_rates")
        if res:
            return Coins.from_data(res)
        else:
            return Coins({})

    async def exchange_rate(self, denom: str) -> Coin:
        """Fetches registered exchange rate of Luna in a specific denom.

        Args:
            denom (str): denom

        Returns:
            Coin: exchange rate of Luna
        """
        rates = await self.exchange_rates()
        return rates[denom]

    async def active_denoms(self) -> List[str]:
        """Fetches current active denoms.

        Returns:
            List[str]: active denoms
        """
        return await self._c._get("/oracle/denoms/actives")

    async def feeder_address(self, validator: ValAddress) -> AccAddress:
        """Fetches associated feeder address for a validator.

        Args:
            validator (ValAddress): validator operator address

        Returns:
            AccAddress: feeder address
        """
        return await self._c._get(f"/oracle/voters/{validator}/feeder")

    async def misses(self, validator: ValAddress) -> int:
        """Fetches current value of miss counter for a validator.

        Args:
            validator (ValAddress): validator operator address

        Returns:
            int: current number of misses
        """
        return int(await self._c._get(f"/oracle/voters/{validator}/miss"))

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
            res = await self._c._get(f"/oracle/voters/{validator}/aggregate_prevote")
        except LCDResponseError as e:
            if e.response.status == 404:
                return None
            else:
                raise e
        return AggregateExchangeRatePrevote.from_data(res)

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
            res = await self._c._get(f"/oracle/voters/{validator}/aggregate_vote")
        except LCDResponseError as e:
            if e.response.status == 404:
                return None
            else:
                raise e
        return AggregateExchangeRateVote.from_data(res)

    async def parameters(self) -> dict:
        """Fetches Oracle module parameters.

        Returns:
            dict: Oracle module parameters
        """
        return await self._c._get("/oracle/parameters")


class OracleAPI(AsyncOracleAPI):
    @sync_bind(AsyncOracleAPI.prevotes)
    def prevotes(
        self, denom: Optional[str] = None, validator: Optional[ValAddress] = None
    ) -> List[ExchangeRatePrevote]:
        pass

    prevotes.__doc__ = AsyncOracleAPI.prevotes.__doc__

    @sync_bind(AsyncOracleAPI.votes)
    def votes(
        self, denom: Optional[str] = None, validator: Optional[ValAddress] = None
    ) -> List[ExchangeRateVote]:
        pass

    votes.__doc__ = AsyncOracleAPI.votes.__doc__

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
