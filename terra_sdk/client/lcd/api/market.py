from ._base import BaseAPI

from terra_sdk.core.dec import Dec
from terra_sdk.core.coin import Coin


class MarketAPI(BaseAPI):
    async def swap_rate(self, offer_coin: Coin, ask_denom: str) -> Coin:
        params = {"offer_coin": str(offer_coin), "ask_denom": ask_denom}
        res = await self._c._get(f"/market/swap", params)
        return Coin.from_data(res.get("result"))

    async def terra_pool_delta(self) -> Dec:
        res = await self._c._get(f"/market/terra_pool_delta")
        return Dec(res.get("result"))
