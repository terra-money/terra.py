from ._base import BaseAPI

from typing import List, Optional


class SlashingAPI(BaseAPI):
    async def signing_infos(self, val_cons_pub_key: Optional[str] = None) -> List[dict]:
        if val_cons_pub_key is None:
            url = f"/slashing/signing_infos"
        else:
            url = f"/slashing/validators/{val_cons_pub_key}/signing_info"
        return await self._c._get(url)

    async def parameters(self) -> dict:
        return await self._c._get("/slashing/parameters")