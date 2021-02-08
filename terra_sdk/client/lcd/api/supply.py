from terra_sdk.core.coins import Coins

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncSupplyAPI", "SupplyAPI"]


class AsyncSupplyAPI(BaseAsyncAPI):
    async def total(self) -> Coins:
        """Fetches the current total supply of all tokens.

        Returns:
            Coins: total supply
        """
        res = await self._c._get("/supply/total")
        return Coins.from_data(res)


class SupplyAPI(AsyncSupplyAPI):
    @sync_bind(AsyncSupplyAPI.total)
    def total(self) -> Coins:
        pass

    total.__doc__ = AsyncSupplyAPI.total.__doc__
