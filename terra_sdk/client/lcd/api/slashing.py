from typing import List, Optional

from terra_sdk.core import ValConsPubKey

from ._base import BaseAPI


class SlashingAPI(BaseAPI):
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
