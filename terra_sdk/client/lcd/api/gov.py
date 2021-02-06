from typing import List

from terra_sdk.core.gov import Proposal

from ._base import BaseAPI


class AsyncGovAPI(BaseAPI):
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


class GovAPI(BaseAPI):
    def proposals(self) -> List[Proposal]:
        """Fetches all proposals.

        Returns:
            List[Proposal]: proposals
        """
        res = self._c._get("/gov/proposals")
        return [Proposal.from_data(d) for d in res]

    def proposal(self, proposal_id: int) -> Proposal:
        """Fetches a single proposal by id.

        Args:
            proposal_id (int): proposal ID

        Returns:
            Proposal: proposal
        """
        res = self._c._get("/gov/proposals/{proposal_id}")
        return Proposal.from_data(res)

    def proposer(self, proposal_id: int) -> str:
        """Fetches the proposer of a proposal.

        Args:
            proposal_id (int): proposal ID

        Returns:
            str: proposal's proposer
        """
        res = self._c._get(f"/gov/proposals/{proposal_id}/proposer")
        return res["proposer"]

    def deposits(self, proposal_id: int):
        """Fetches the deposit information about a proposal.

        Args:
            proposal_id (int): proposal ID
        """
        return self._c._get(f"/gov/proposals/{proposal_id}/deposits")

    def votes(self, proposal_id: int):
        """Fetches the votes for a proposal.

        Args:
            proposal_id (int): proposal ID
        """
        return self._c._get(f"/gov/proposals/{proposal_id}/votes")

    def tally(self, proposal_id: int):
        """Fetches the tally for a proposal.

        Args:
            proposal_id (int): proposal ID
        """
        return self._c._get(f"/gov/proposals/{proposal_id}/tally")

    def deposit_parameters(self) -> dict:
        """Fetches the Gov module's deposit parameters.

        Returns:
            dict: deposit parameters
        """
        return self._c._get("/gov/parameters/deposit")

    def voting_parameters(self) -> dict:
        """Fetches the Gov module's voting parameters.

        Returns:
            dict: voting parameters
        """
        return self._c._get("/gov/parameters/voting")

    def tally_parameters(self) -> dict:
        """Fetches the Gov module's tally parameters.

        Returns:
            dict: tally parameters
        """
        return self._c._get("/gov/parameters/tallying")

    def parameters(self) -> dict:
        """Fetches the Gov module's parameters.

        Returns:
            dict: Gov module parameters
        """
        return {
            "deposit_params": self.deposit_parameters(),
            "voting_params": self.voting_parameters(),
            "tally_params": self.tally_parameters(),
        }
