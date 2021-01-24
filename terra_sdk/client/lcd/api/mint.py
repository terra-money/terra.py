from ._base import BaseAPI


class MintAPI(BaseAPI):
    async def proposals(self):
        return await self._c._get(f"/gov/proposals")
