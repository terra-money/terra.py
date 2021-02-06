from terra_sdk.core import AccAddress, Coins

from ._base import BaseAPI


class AsyncBankAPI(BaseAPI):
    async def balance(self, address: AccAddress) -> Coins:
        res = await self._c._get(f"/bank/balances/{address}")
        return Coins.from_data(res)


class BankAPI(BaseAPI):
    def balance(self, address: AccAddress) -> Coins:
        """Fetches the current balance of an account.

        Args:
            address (AccAddress): account address

        Returns:
            Coins: balance
        """
        res = self._c._get(f"/bank/balances/{address}")
        return Coins.from_data(res)
