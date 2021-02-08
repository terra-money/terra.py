import wrapt


class BaseAsyncAPI:
    # c = AsyncLCDClient
    def __init__(self, c):
        self._c = c

    def _run_sync(self, coroutine):
        """Runs an asynchronous coroutine synchronously."""
        return self._c.loop.run_until_complete(coroutine)


def sync_bind(async_call):
    @wrapt.decorator
    def decorator(wrapped, instance, args, kwargs):
        return instance._run_sync(async_call(instance, *args, *kwargs))

    return decorator
