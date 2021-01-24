from ._base import BaseAPI


class MintAPI(BaseAPI):
    async def proposals(self):
        res = await self._c._get(f"/gov/proposals")
        return res["result"]
