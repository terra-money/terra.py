from terra_sdk.core import Coin, Dec

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncMarketAPI", "MarketAPI"]


class AsyncMarketAPI(BaseAsyncAPI):
    async def swap_rate(self, offer_coin: Coin, ask_denom: str) -> Coin:
        """Simulates a swap given an amount offered and a target denom.

        Args:
            offer_coin (Coin): amount offered (swap from)
            ask_denom (str): target denom (swap to)

        Returns:
            Coin: simulated amount received
        """
        params = {"offer_coin": str(offer_coin), "ask_denom": ask_denom}
        res = await self._c._get("/market/swap", params)
        return Coin.from_data(res)

    async def terra_pool_delta(self) -> Dec:
        """Fetches the Terra pool delta.

        Returns:
            Dec: Terra pool delta
        """
        res = await self._c._get("/market/terra_pool_delta")
        return Dec(res)

    async def parameters(self) -> dict:
        """Fetches the Market module's parameters.

        Returns:
            dict: Market module parameters
        """
        return await self._c._get("/market/parameters")


class MarketAPI(AsyncMarketAPI):
    @sync_bind(AsyncMarketAPI.swap_rate)
    def swap_rate(self, offer_coin: Coin, ask_denom: str) -> Coin:
        pass

    swap_rate.__doc__ = AsyncMarketAPI.swap_rate.__doc__

    @sync_bind(AsyncMarketAPI.terra_pool_delta)
    def terra_pool_delta(self) -> Dec:
        pass

    terra_pool_delta.__doc__ = AsyncMarketAPI.terra_pool_delta.__doc__

    @sync_bind(AsyncMarketAPI.parameters)
    def parameters(self) -> dict:
        pass

    parameters.__doc__ = AsyncMarketAPI.parameters.__doc__
