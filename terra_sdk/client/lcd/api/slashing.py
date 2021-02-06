from typing import List, Optional

from terra_sdk.core import ValConsPubKey

from ._base import BaseAPI


class AsyncSlashingAPI(BaseAPI):
    async def signing_infos(
        self, val_cons_pub_key: Optional[ValConsPubKey] = None
    ) -> List[dict]:
        if val_cons_pub_key is None:
            url = "/slashing/signing_infos"
        else:
            url = f"/slashing/validators/{val_cons_pub_key}/signing_info"
        return await self._c._get(url)

    async def parameters(self) -> dict:
        return await self._c._get("/slashing/parameters")


class SlashingAPI(BaseAPI):
    def signing_infos(
        self, val_cons_pub_key: Optional[ValConsPubKey] = None
    ) -> List[dict]:
        """Fetches signing infos, optionally filtering by validator consensus public key.

        Args:
            val_cons_pub_key (Optional[ValConsPubKey], optional): validator consensus public key. Defaults to None.

        Returns:
            List[dict]: signing infos
        """
        if val_cons_pub_key is None:
            url = "/slashing/signing_infos"
        else:
            url = f"/slashing/validators/{val_cons_pub_key}/signing_info"
        return self._c._get(url)

    def parameters(self) -> dict:
        """Fetches Slashing module parameters.

        Returns:
            dict: Slashing module parameters
        """
        return self._c._get("/slashing/parameters")
