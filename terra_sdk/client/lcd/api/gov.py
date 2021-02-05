from typing import List

from terra_sdk.core.gov import Proposal

from ._base import BaseAPI


class GovAPI(BaseAPI):
    async def proposals(self) -> List[Proposal]:
        res = await self._c._get("/gov/proposals")
        return [Proposal.from_data(d) for d in res]

    async def proposal(self, proposal_id: int) -> Proposal:
        res = await self._c._get("/gov/proposals/{proposal_id}")
        return Proposal.from_data(res)

    async def proposer(self, proposal_id: int) -> str:
        res = await self._c._get(f"/gov/proposals/{proposal_id}/proposer")
        return res["proposer"]

    async def deposits(self, proposal_id: int):
        return await self._c._get(f"/gov/proposals/{proposal_id}/deposits")

    async def votes(self, proposal_id: int):
        return await self._c._get(f"/gov/proposals/{proposal_id}/votes")

    async def tally(self, proposal_id: int):
        return await self._c._get(f"/gov/proposals/{proposal_id}/tally")

    async def deposit_parameters(self) -> dict:
        return await self._c._get("/gov/parameters/deposit")

    async def voting_parameters(self) -> dict:
        return await self._c._get("/gov/parameters/voting")

    async def tally_parameters(self) -> dict:
        return await self._c._get("/gov/parameters/tallying")

    async def parameters(self) -> dict:
        return {
            "deposit_params": await self.deposit_parameters(),
            "voting_params": await self.voting_parameters(),
            "tally_params": await self.tally_parameters(),
        }
