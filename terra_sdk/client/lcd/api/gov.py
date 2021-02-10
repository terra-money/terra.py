from typing import List

from terra_sdk.core.gov import Proposal

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncGovAPI", "GovAPI"]


class AsyncGovAPI(BaseAsyncAPI):
    async def proposals(self) -> List[Proposal]:
        """Fetches all proposals.

        Returns:
            List[Proposal]: proposals
        """
        res = await self._c._get("/gov/proposals")
        return [Proposal.from_data(d) for d in res]

    async def proposal(self, proposal_id: int) -> Proposal:
        """Fetches a single proposal by id.

        Args:
            proposal_id (int): proposal ID

        Returns:
            Proposal: proposal
        """
        res = await self._c._get("/gov/proposals/{proposal_id}")
        return Proposal.from_data(res)

    async def proposer(self, proposal_id: int) -> str:
        """Fetches the proposer of a proposal.

        Args:
            proposal_id (int): proposal ID

        Returns:
            str: proposal's proposer
        """
        res = await self._c._get(f"/gov/proposals/{proposal_id}/proposer")
        return res["proposer"]

    async def deposits(self, proposal_id: int):
        """Fetches the deposit information about a proposal.

        Args:
            proposal_id (int): proposal ID
        """
        return await self._c._get(f"/gov/proposals/{proposal_id}/deposits")

    async def votes(self, proposal_id: int):
        """Fetches the votes for a proposal.

        Args:
            proposal_id (int): proposal ID
        """
        return await self._c._get(f"/gov/proposals/{proposal_id}/votes")

    async def tally(self, proposal_id: int):
        """Fetches the tally for a proposal.

        Args:
            proposal_id (int): proposal ID
        """
        return await self._c._get(f"/gov/proposals/{proposal_id}/tally")

    async def deposit_parameters(self) -> dict:
        """Fetches the Gov module's deposit parameters.

        Returns:
            dict: deposit parameters
        """
        return await self._c._get("/gov/parameters/deposit")

    async def voting_parameters(self) -> dict:
        """Fetches the Gov module's voting parameters.

        Returns:
            dict: voting parameters
        """
        return await self._c._get("/gov/parameters/voting")

    async def tally_parameters(self) -> dict:
        """Fetches the Gov module's tally parameters.

        Returns:
            dict: tally parameters
        """
        return await self._c._get("/gov/parameters/tallying")

    async def parameters(self) -> dict:
        """Fetches the Gov module's parameters.

        Returns:
            dict: Gov module parameters
        """
        return {
            "deposit_params": await BaseAsyncAPI._try_await(self.deposit_parameters()),
            "voting_params": await BaseAsyncAPI._try_await(self.voting_parameters()),
            "tally_params": await BaseAsyncAPI._try_await(self.tally_parameters()),
        }


class GovAPI(AsyncGovAPI):
    @sync_bind(AsyncGovAPI.proposals)
    def proposals(self) -> List[Proposal]:
        pass

    proposals.__doc__ = AsyncGovAPI.proposals.__doc__

    @sync_bind(AsyncGovAPI.proposal)
    def proposal(self, proposal_id: int) -> Proposal:
        pass

    proposal.__doc__ = AsyncGovAPI.proposal.__doc__

    @sync_bind(AsyncGovAPI.proposer)
    def proposer(self, proposal_id: int) -> str:
        pass

    proposer.__doc__ = AsyncGovAPI.proposer.__doc__

    @sync_bind(AsyncGovAPI.deposits)
    def deposits(self, proposal_id: int):
        pass

    deposits.__doc__ = AsyncGovAPI.deposits.__doc__

    @sync_bind(AsyncGovAPI.votes)
    def votes(self, proposal_id: int):
        pass

    votes.__doc__ = AsyncGovAPI.votes.__doc__

    @sync_bind(AsyncGovAPI.tally)
    def tally(self, proposal_id: int):
        pass

    tally.__doc__ = AsyncGovAPI.tally.__doc__

    @sync_bind(AsyncGovAPI.deposit_parameters)
    def deposit_parameters(self) -> dict:
        pass

    deposits.__doc__ = AsyncGovAPI.deposit_parameters.__doc__

    @sync_bind(AsyncGovAPI.voting_parameters)
    def voting_parameters(self) -> dict:
        pass

    voting_parameters.__doc__ = AsyncGovAPI.voting_parameters.__doc__

    @sync_bind(AsyncGovAPI.tally_parameters)
    def tally_parameters(self) -> dict:
        pass

    tally_parameters.__doc__ = AsyncGovAPI.tally_parameters.__doc__

    @sync_bind(AsyncGovAPI.parameters)
    def parameters(self) -> dict:
        pass

    parameters.__doc__ = AsyncGovAPI.parameters.__doc__
