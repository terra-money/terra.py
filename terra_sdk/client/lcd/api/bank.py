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
        res = await self._c._get(f"/cosmos/bank/v1beta1/balances/{address}")
        return Coins.from_data(res["balances"])

    async def total(self) -> Coins:
        """Fetches the current total supply of all tokens.

        Returns:
            Coins: total supply
        """
        res = await self._c._get("/cosmos/bank/v1beta1/supply")
        return Coins.from_data(res.get("supply"))


class BankAPI(AsyncBankAPI):
    @sync_bind(AsyncBankAPI.balance)
    def balance(self, address: AccAddress) -> Coins:
        pass

    balance.__doc__ = AsyncBankAPI.balance.__doc__

    @sync_bind(AsyncBankAPI.total)
    def total(self) -> Coins:
        pass

    total.__doc__ = AsyncBankAPI.total.__doc__

