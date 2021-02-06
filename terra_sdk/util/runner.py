import asyncio
from typing import Any, Callable

from terra_sdk.client.lcd import AsyncLCDClient

__all__ = ["run_with_async_client"]


async def _run(
    loop: asyncio.AbstractEventLoop, fn: Callable[[AsyncLCDClient], Any], **kwargs
):
    async with AsyncLCDClient(loop=loop, **kwargs) as terra:
        await fn(terra)


def run_with_async_client(fn: Callable[[AsyncLCDClient], Any], **kwargs):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(_run(loop, fn, **kwargs))
