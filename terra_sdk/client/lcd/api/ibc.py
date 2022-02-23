from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncIbcAPI", "IbcAPI"]


class AsyncIbcAPI(BaseAsyncAPI):
    async def parameters(self) -> dict:
        """Fetches the Ibc module's parameters.

        Returns:
            List: allowed clients
        """
        res = await self._c._get("/ibc/client/v1/params")
        return res["params"]

    # TODO: functions for clients, connections and channels


class IbcAPI(AsyncIbcAPI):
    @sync_bind(AsyncIbcAPI.parameters)
    def parameters(self) -> dict:
        pass

    parameters.__doc__ = AsyncIbcAPI.parameters.__doc__
