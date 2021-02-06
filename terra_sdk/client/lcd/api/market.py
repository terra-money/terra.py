from terra_sdk.core import Coin, Dec

from ._base import BaseAPI


class AsyncMarketAPI(BaseAPI):
    def swap_rate(self, offer_coin: Coin, ask_denom: str) -> Coin:
        params = {"offer_coin": str(offer_coin), "ask_denom": ask_denom}
        res = self._c._get("/market/swap", params)
        return Coin.from_data(res)

    def terra_pool_delta(self) -> Dec:
        res = self._c._get("/market/terra_pool_delta")
        return Dec(res)

    def parameters(self) -> dict:
        return self._c._get("/market/parameters")


class MarketAPI(BaseAPI):
    def swap_rate(self, offer_coin: Coin, ask_denom: str) -> Coin:
        params = {"offer_coin": str(offer_coin), "ask_denom": ask_denom}
        res = self._c._get("/market/swap", params)
        return Coin.from_data(res)

    def terra_pool_delta(self) -> Dec:
        res = self._c._get("/market/terra_pool_delta")
        return Dec(res)

    def parameters(self) -> dict:
        return self._c._get("/market/parameters")
