from terra_sdk.core import Coin, Dec

from ._base import BaseAPI


class MarketAPI(BaseAPI):
    async def swap_rate(self, offer_coin: Coin, ask_denom: str) -> Coin:
        params = {"offer_coin": str(offer_coin), "ask_denom": ask_denom}
        res = await self._c._get("/market/swap", params)
        return Coin.from_data(res)

    async def terra_pool_delta(self) -> Dec:
        res = await self._c._get("/market/terra_pool_delta")
        return Dec(res)

    async def parameters(self) -> dict:
        return await self._c._get("/market/parameters")
