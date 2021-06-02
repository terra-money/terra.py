from typing import List

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncSlashingAPI", "SlashingAPI"]


class AsyncSlashingAPI(BaseAsyncAPI):
    async def signing_infos(self) -> List[dict]:
        """Fetches signing infos.

        Returns:
            List[dict]: signing infos
        """
        return await self._c._get("/slashing/signing_infos")

    async def parameters(self) -> dict:
        """Fetches Slashing module parameters.

        Returns:
            dict: Slashing module parameters
        """
        return await self._c._get("/slashing/parameters")


class SlashingAPI(AsyncSlashingAPI):
    @sync_bind(AsyncSlashingAPI.signing_infos)
    def signing_infos(self) -> List[dict]:
        pass

    signing_infos.__doc__ = AsyncSlashingAPI.signing_infos.__doc__

    @sync_bind(AsyncSlashingAPI.parameters)
    def parameters(self) -> dict:
        pass

    parameters.__doc__ = AsyncSlashingAPI.parameters.__doc__
