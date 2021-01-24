from .base_api import BaseAPI

from terra_sdk.core.coins import Coins


class BankAPI(BaseAPI):
    async def balance(self, address) -> Coins:
        res = await self._c.get(f"/bank/balances/{address}")
        return Coins.from_data(res)
