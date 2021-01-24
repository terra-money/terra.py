from ._base import BaseAPI

from terra_sdk.core.coins import Coins


class SupplyAPI(BaseAPI):
    async def total(self) -> Coins:
        res = await self._c._get(f"/supply/total")
        return Coins.from_data(res)
