from ._base import BaseAPI


class GovAPI(BaseAPI):
    async def proposals(self):
        return await self._c._get(f"/gov/proposals")

    async def proposal(self, proposal_id: int):
        return await self._c._get(f"/gov/proposals/{proposal_id}")

    async def proposer(self, proposal_id: int):
        return await self._c._get(f"/gov/proposals/{proposal_id}/proposer")
