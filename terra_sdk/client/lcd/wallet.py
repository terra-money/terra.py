from __future__ import annotations

from terra_sdk.core.auth import StdSignMsg, StdTx
from terra_sdk.key.key import Key

__all__ = ["Wallet", "AsyncWallet"]


class AsyncWallet:
    def __init__(self, lcd, key: Key):
        self.lcd = lcd
        self.key = key

    async def account_number(self) -> int:
        res = await self.lcd.auth.account_info(self.key.acc_address)
        return res.account_number

    async def sequence(self) -> int:
        res = await self.lcd.auth.account_info(self.key.acc_address)
        return res.sequence

    async def account_number_and_sequence(self) -> dict:
        res = await self.lcd.auth.account_info(self.key.acc_address)
        return {"account_number": res.account_number, "sequence": res.sequence}

    async def create_tx(self, *args, **kwargs) -> StdSignMsg:
        return await self.lcd.tx.create(self.key.acc_address, *args, **kwargs)

    async def create_and_sign_tx(self, *args, **kwargs) -> StdTx:
        tx = await self.create_tx(*args, **kwargs)
        return self.key.sign_tx(tx)


class Wallet:
    def __init__(self, lcd, key: Key):
        self.lcd = lcd
        self.key = key

    def account_number(self) -> int:
        res = self.lcd.auth.account_info(self.key.acc_address)
        return res.account_number

    def sequence(self) -> int:
        res = self.lcd.auth.account_info(self.key.acc_address)
        return res.sequence

    def account_number_and_sequence(self) -> dict:
        res = self.lcd.auth.account_info(self.key.acc_address)
        return {"account_number": res.account_number, "sequence": res.sequence}

    def create_tx(self, *args, **kwargs) -> StdSignMsg:
        return self.lcd.tx.create(self.key.acc_address, *args, **kwargs)

    def create_and_sign_tx(self, *args, **kwargs) -> StdTx:
        return self.key.sign_tx(self.create_tx(*args, **kwargs))
