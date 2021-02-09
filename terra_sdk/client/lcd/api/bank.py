from terra_sdk.core import AccAddress, Coins

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncBankAPI", "BankAPI"]


class AsyncBankAPI(BaseAsyncAPI):
    async def balance(self, address: AccAddress) -> Coins:
        """Fetches an account's current balance.

        Args:
            address (AccAddress): account address

        Returns:
            Coins: balance
        """
        res = await self._c._get(f"/bank/balances/{address}")
        return Coins.from_data(res)


class BankAPI(AsyncBankAPI):
    @sync_bind(AsyncBankAPI.balance)
    def balance(self, address: AccAddress) -> Coins:
        pass

    balance.__doc__ = AsyncBankAPI.balance.__doc__
