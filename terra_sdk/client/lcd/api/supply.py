from terra_sdk.core.coins import Coins

from ._base import BaseAPI


class AsyncSupplyAPI(BaseAPI):
    async def total(self) -> Coins:
        res = await self._c._get("/supply/total")
        return Coins.from_data(res)


class SupplyAPI(BaseAPI):
    def total(self) -> Coins:
        """Fetches the current total supply of all tokens.

        Returns:
            Coins: total supply
        """
        res = self._c._get("/supply/total")
        return Coins.from_data(res)
