from typing import Optional

from terra_sdk.core import Dec, Numeric

from ._base import BaseAsyncAPI, sync_bind
from ..params import APIParams
__all__ = ["AsyncMintAPI", "MintAPI"]


class AsyncMintAPI(BaseAsyncAPI):
    async def inflation(self, params: Optional[APIParams] = None) -> Dec:
        """Fetches the current inflation.

        Args:
            params (APIParams): optional parameters

        Returns:
            Dec: inflation
        """
        res = await self._c._get("/cosmos/mint/v1beta1/inflation", params)
        return Dec(res.get("inflation"))

    async def annual_provisions(self, params: Optional[APIParams] = None) -> Dec:
        """Fetches the annual provisions.

        Args:
            params (APIParams): optional parameters

        Returns:
            Dec: annual provisions
        """
        res = await self._c._get("/cosmos/mint/v1beta1/annual_provisions", params)
        return Dec(res.get("annual_provisions"))

    async def parameters(self, params: Optional[APIParams] = None) -> dict:
        """Fetches the Mint module's parameters.

        Args:
            params (APIParams): optional parameters

        Returns:
            dict: Mint module parameters
        """
        res = await self._c._get("/cosmos/mint/v1beta1/params", params)
        params = res.get("params")
        return {
            "mint_denom": params["mint_denom"],
            "inflation_rate_change": Dec(params["inflation_rate_change"]),
            "inflation_max": Dec(params["inflation_max"]),
            "inflation_min": Dec(params["inflation_min"]),
            "goal_bonded": Dec(params["goal_bonded"]),
            "blocks_per_year": Numeric.parse(params["blocks_per_year"]),
        }


class MintAPI(AsyncMintAPI):
    @sync_bind(AsyncMintAPI.inflation)
    def inflation(self, params: Optional[APIParams] = None) -> Dec:
        pass

    inflation.__doc__ = AsyncMintAPI.inflation.__doc__

    @sync_bind(AsyncMintAPI.annual_provisions)
    def annual_provisions(self, params: Optional[APIParams] = None) -> Dec:
        pass

    annual_provisions.__doc__ = AsyncMintAPI.annual_provisions.__doc__

    @sync_bind(AsyncMintAPI.parameters)
    def parameters(self, params: Optional[APIParams] = None) -> dict:
        pass

    parameters.__doc__ = AsyncMintAPI.parameters.__doc__
