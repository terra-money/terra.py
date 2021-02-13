import asyncio

import wrapt


class BaseAsyncAPI:
    # c = AsyncLCDClient
    def __init__(self, c):
        self._c = c

    def _run_sync(self, coroutine):
        """Runs an asynchronous coroutine synchronously."""
        return self._c.loop.run_until_complete(coroutine)

    @staticmethod
    async def _try_await(aw):
        """Checks if aw is a coroutine object and awaits it if so. Otherwise, just returns."""
        if asyncio.iscoroutine(aw):
            return await aw
        else:
            return aw


def sync_bind(async_call):
    """A decorator that redirects the function to the synchronous version of async_call."""

    @wrapt.decorator
    def decorator(wrapped, instance, args, kwargs):
        return instance._run_sync(async_call(instance, *args, **kwargs))

    return decorator
