import warnings
from typing import Optional, Union

from terra_sdk.client.lcd.api import ApiResponse, BaseApi, project
from terra_sdk.core import Coin, Dec
from terra_sdk.util.serdes import terra_sdkBox

__all__ = ["MarketApi"]


class MarketApi(BaseApi):
    def swap_rate(self, offer_coin: Coin, ask_denom: str) -> Union[ApiResponse, Coin]:
        if type(offer_coin.amount) != int:
            warnings.warn(
                f"Coin's amount will be converted to integer: {int(offer_coin.amount)} {offer_coin.denom}",
                SyntaxWarning,
            )
        params = {
            "offer_coin": f"{int(offer_coin.amount)}{offer_coin.denom}",
            "ask_denom": ask_denom,
        }
        res = self._api_get(f"/market/swap", params=params)
        return project(res, Coin.deserialize(res))

    def terra_pool_delta(self) -> Union[ApiResponse, Dec]:
        res = self._api_get("/market/terra_pool_delta")
        return project(res, Dec.deserialize(res))

    def params(self, key: Optional[str] = None) -> Union[ApiResponse, Dec, dict]:
        res = self._api_get("/market/parameters")
        p = terra_sdkBox(res)
        p["pool_recovery_period"] = int(p["pool_recovery_period"])
        p["base_pool"] = Dec.deserialize(p["base_pool"])
        p["min_spread"] = Dec.deserialize(p["min_spread"])
        p["tobin_tax"] = Dec.deserialize(p["tobin_tax"])
        ill = p["illiquid_tobin_tax_list"]
        p["illiquid_tobin_tax_list"] = terra_sdkBox({})
        for item in ill:
            p["illiquid_tobin_tax_list"][item["denom"]] = Dec(item["tax_rate"])
        return project(res, p[key] if key else p)
