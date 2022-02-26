from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncIbcTransferAPI", "IbcTransferAPI"]


class AsyncIbcTransferAPI(BaseAsyncAPI):
    async def parameters(self) -> dict:
        """Fetches the IbcTransfer module's parameters.

        Returns:
            dict: IbcTransfer module parameters
        """
        res = await self._c._get("/ibc/apps/transfer/v1/params")
        params = res["params"]
        return {
            "send_enabled": bool(params["send_enabled"]),
            "receive_enabled": bool(params["receive_enabled"]),
        }


class IbcTransferAPI(AsyncIbcTransferAPI):
    @sync_bind(AsyncIbcTransferAPI.parameters)
    def parameters(self) -> dict:
        pass

    parameters.__doc__ = AsyncIbcTransferAPI.parameters.__doc__
