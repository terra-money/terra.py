from ._base import BaseAPI


class SlashingAPI(BaseAPI):
    async def proposals(self):
        res = await self._c._get(f"/gov/proposals")
        return res["result"]
