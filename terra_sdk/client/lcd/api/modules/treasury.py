from typing import Optional, Union

from terra_sdk.client.lcd.api import ApiResponse, BaseApi, project
from terra_sdk.core import Coin, Coins, Dec, PolicyConstraints
from terra_sdk.core.denoms import uLuna
from terra_sdk.util.serdes import terra_sdkBox

__all__ = ["TreasuryApi"]


class TreasuryApi(BaseApi):
    def tax_cap(self, denom: str) -> Union[ApiResponse, Coin]:
        res = self._api_get(f"/treasury/tax_cap/{denom}")
        return project(res, Coin(denom, res))

    def tax_rate(self) -> Union[ApiResponse, Dec]:
        res = self._api_get("/treasury/tax_rate")  # tr
        return project(res, Dec.deserialize(res))

    def reward_weight(self) -> Union[ApiResponse, Dec]:
        res = self._api_get("/treasury/reward_weight")  # rw
        return project(res, Dec.deserialize(res))

    def tax_proceeds(self, denom: Optional[str] = None) -> Union[ApiResponse, Coins]:
        res = self._api_get("/treasury/tax_proceeds")
        tax_proceeds = Coins.deserialize(res)
        return project(res, tax_proceeds[denom] if denom else tax_proceeds)

    def seigniorage_proceeds(self) -> Union[ApiResponse, Coin]:
        res = self._api_get("/treasury/seigniorage_proceeds")
        return project(res, Coin(uLuna, int(res)))

    def params(self, key: Optional[str] = None) -> Union[ApiResponse, Dec, int, dict]:
        res = self._api_get("/treasury/parameters")
        p = terra_sdkBox(
            res,
            box_recast={
                "seigniorage_burden_target": Dec,
                "mining_increment": Dec,
                "window_short": int,
                "window_long": int,
                "window_probation": int,
            },
        )
        p["tax_policy"] = PolicyConstraints.deserialize(p["tax_policy"])
        p["reward_policy"] = PolicyConstraints.deserialize(p["reward_policy"])
        return project(res, p[key] if key else p)
