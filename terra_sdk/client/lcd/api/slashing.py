from typing import List, Optional

from terra_sdk.core import ValConsPubKey

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncSlashingAPI", "SlashingAPI"]


class AsyncSlashingAPI(BaseAsyncAPI):
    async def signing_infos(
        self, val_cons_pub_key: Optional[ValConsPubKey] = None
    ) -> List[dict]:
        """Fetches signing infos, optionally filtering by validator consensus public key.

        Args:
            val_cons_pub_key (Optional[ValConsPubKey], optional): validator consensus public key.

        Returns:
            List[dict]: signing infos
        """
        if val_cons_pub_key is None:
            url = "/slashing/signing_infos"
        else:
            url = f"/slashing/validators/{val_cons_pub_key}/signing_info"
        return await self._c._get(url)

    async def parameters(self) -> dict:
        """Fetches Slashing module parameters.

        Returns:
            dict: Slashing module parameters
        """
        return await self._c._get("/slashing/parameters")


class SlashingAPI(AsyncSlashingAPI):
    @sync_bind(AsyncSlashingAPI.signing_infos)
    def signing_infos(
        self, val_cons_pub_key: Optional[ValConsPubKey] = None
    ) -> List[dict]:
        pass

    signing_infos.__doc__ = AsyncSlashingAPI.signing_infos.__doc__

    @sync_bind(AsyncSlashingAPI.parameters)
    def parameters(self) -> dict:
        pass

    parameters.__doc__ = AsyncSlashingAPI.parameters.__doc__
