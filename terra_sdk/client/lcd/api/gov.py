from typing import List

from ._base import BaseAPI


class GovAPI(BaseAPI):
    async def proposals(self) -> List[dict]:
        return await self._c._get(f"/gov/proposals")

    async def proposal(self, proposal_id: int) -> dict:
        return await self._c._get(f"/gov/proposals/{proposal_id}")

    async def proposer(self, proposal_id: int) -> str:
        return await self._c._get(f"/gov/proposals/{proposal_id}/proposer")

    async def deposits(self, proposal_id: int):
        return await self._c._get(f"/gov/proposals/{proposal_id}/deposits")

    async def votes(self, proposal_id: int):
        return await self._c._get(f"/gov/proposals/{proposal_id}/votes")

    async def tally(self, proposal_id: int):
        return await self._c._get(f"/gov/proposals/{proposal_id}/tally")

    async def deposit_parameters(self) -> dict:
        return await self._c._get(f"/gov/parameters/deposit")

    async def voting_parameters(self) -> dict:
        return await self._c._get(f"/gov/parameters/voting")

    async def tally_parameters(self) -> dict:
        return await self._c._get(f"/gov/parameters/tally")

    async def parameters(self) -> dict:
        return {
            "deposit_params": await self.deposit_parameters(),
            "voting_params": await self.voting_parameters(),
            "tally_params": await self.tally_parameters(),
        }
