from terra_sdk.core import AccAddress, Coins

from ._base import BaseAPI


class BankAPI(BaseAPI):
    async def balance(self, address: AccAddress) -> Coins:
        res = await self._c._get(f"/bank/balances/{address}")
        return Coins.from_data(res)
