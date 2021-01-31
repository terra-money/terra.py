from ._base import BaseAPI

from terra_sdk.core import Coins


class BankAPI(BaseAPI):
    async def balance(self, address) -> Coins:
        res = await self._c._get(f"/bank/balances/{address}")
        return Coins.from_data(res)
