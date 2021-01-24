from .base_api import BaseAPI


class GovAPI(BaseAPI):
    async def proposals(self):
        res = await self._c.get(f"/gov/proposals")
        return res["result"]

    async def proposal(self, proposal_id: int):
        res = await self._c.get(f"/gov/proposals/{proposal_id}")
        return res["result"]

    async def proposer(self, proposal_id: int):
        res = await self._c.get(f"/gov/proposals/{proposal_id}/proposer")
        return res["result"]
