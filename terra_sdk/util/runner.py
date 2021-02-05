import asyncio
from typing import Callable, Any

from terra_sdk.client.lcd import LCDClient

__all__ = ["run_with_lcdclient"]


async def _run(
    loop: asyncio.AbstractEventLoop, fn: Callable[[LCDClient], Any], **kwargs
):
    async with LCDClient(loop=loop, **kwargs) as terra:
        await fn(terra)


def run_with_lcdclient(fn: Callable[[LCDClient], Any], **kwargs):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(_run(loop, fn, **kwargs))
