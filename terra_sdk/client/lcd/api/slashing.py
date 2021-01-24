from .base_api import BaseAPI


class SlashingAPI(BaseAPI):
    async def proposals(self):
        res = await self._c.get(f"/gov/proposals")
        return res["result"]
