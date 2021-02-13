from terra_sdk.core import Dec

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncMintAPI", "MintAPI"]


class AsyncMintAPI(BaseAsyncAPI):
    async def inflation(self) -> Dec:
        """Fetches the current inflation.

        Returns:
            Dec: inflation
        """
        return Dec(await self._c._get("/minting/inflation"))

    async def annual_provisions(self) -> Dec:
        """Fetches the annual provisions.

        Returns:
            Dec: annual provisions
        """
        return Dec(await self._c._get("/minting/annual-provisions"))

    async def parameters(self) -> dict:
        """Fetches the Mint module's parameters.

        Returns:
            dict: Mint module parameters
        """
        return await self._c._get("/minting/parameters")


class MintAPI(AsyncMintAPI):
    @sync_bind(AsyncMintAPI.inflation)
    def inflation(self) -> Dec:
        pass

    inflation.__doc__ = AsyncMintAPI.inflation.__doc__

    @sync_bind(AsyncMintAPI.annual_provisions)
    def annual_provisions(self) -> Dec:
        pass

    annual_provisions.__doc__ = AsyncMintAPI.annual_provisions.__doc__

    @sync_bind(AsyncMintAPI.parameters)
    def parameters(self) -> dict:
        pass

    parameters.__doc__ = AsyncMintAPI.parameters.__doc__
