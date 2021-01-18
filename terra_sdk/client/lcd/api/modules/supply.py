from typing import Union

from terra_sdk.client.lcd.api import ApiResponse, BaseApi, project
from terra_sdk.core import Coins

__all__ = ["SupplyApi"]


class SupplyApi(BaseApi):
    def total(self) -> Union[ApiResponse, Coins]:
        res = self._api_get("/supply/total")
        return project(res, Coins.deserialize(res))
