from terra_sdk.core.coins import Coins

from ._base import BaseAPI


class SupplyAPI(BaseAPI):
    async def total(self) -> Coins:
        res = await self._c._get(f"/supply/total")
        return Coins.from_data(res)
