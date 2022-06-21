from terra_sdk.core import Dec, Numeric
from ._base import BaseAsyncAPI, sync_bind
from ..params import APIParams
from typing import List, Optional

class AsyncAnteAPI(BaseAsyncAPI):
    async def minimum_commission(
        self,
        params: Optional[APIParams] = None,
    ) -> Dec:
        """Fetches the minimum commission.
        Args:
            params (APIParams): optional parameters

        Returns:
            Dec : minimum_commission
        """

        res = await self._c._get("/terra/ante/v2/minimum_commission",params)
        return Dec(res.get("minimum_commission"))


    async def parameters(self, params: Optional[APIParams] = None) -> dict:
        """Fetches the ante module parameters.
        Args:
            params (APIParams): optional parameters

        Returns:
            dict: Distribution module parameters
        """
        res = await self._c._get("/terra/ante/v2/params", params)
        params = res.get("params")
        return {
            "minimum_commission_enforced": Dec(params["minimum_commission_enforced"])
        }

class AnteAPI(AsyncAnteAPI):
    @sync_bind(AsyncAnteAPI.minimum_commission)
    def minimum_commission(self, params: Optional[APIParams] = None) -> Dec:
        pass

    minimum_commission.__doc__ = AsyncAnteAPI.minimum_commission.__doc__

    @sync_bind(AsyncAnteAPI.parameters)
    def parameters(self, params: Optional[APIParams] = None) -> dict:
        pass

    parameters.__doc__ = AsyncAnteAPI.parameters.__doc__
