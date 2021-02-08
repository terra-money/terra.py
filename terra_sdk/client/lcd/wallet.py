from __future__ import annotations

import wrapt
import asyncio

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

    def _run_sync(self, coroutine):
        """Runs an asynchronous coroutine synchronously."""
        return asyncio.get_event_loop().run_until_complete(coroutine)


def sync_bind(async_call):
    @wrapt.decorator
    def decorator(wrapped, instance, args, kwargs):
        return instance._run_sync(async_call(instance, *args, *kwargs))

    return decorator


class Wallet(AsyncWallet):
    @sync_bind(AsyncWallet.account_number)
    def account_number(self) -> int:
        pass

    @sync_bind(AsyncWallet.sequence)
    def sequence(self) -> int:
        pass

    @sync_bind(AsyncWallet.account_number_and_sequence)
    def account_number_and_sequence(self) -> dict:
        pass

    @sync_bind(AsyncWallet.create_tx)
    def create_tx(self, *args, **kwargs) -> StdSignMsg:
        pass

    @sync_bind(AsyncWallet.create_and_sign_tx)
    def create_and_sign_tx(self, *args, **kwargs) -> StdTx:
        pass
