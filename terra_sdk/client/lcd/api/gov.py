from typing import List

from terra_sdk.core.gov import Proposal, ProposalStatus
from terra_sdk.core import Deposit, Coins, Numeric, Dec

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncGovAPI", "GovAPI"]


class AsyncGovAPI(BaseAsyncAPI):
    async def proposals(self, options: dict = {}) -> List[Proposal]:
        """Fetches all proposals.

        Args:
            options (dict, optional): dictionary containing options. Defaults to {}.

        Returns:
            List[Proposal]: proposals
        """
        res = await self._c._get("/cosmos/gov/v1beta1/proposals", options)
        return [Proposal.from_data(d) for d in res.get("proposals")]

    async def proposal(self, proposal_id: int) -> Proposal:
        """Fetches a single proposal by id.

        Args:
            proposal_id (int): proposal ID

        Returns:
            Proposal: proposal
        """
        res = await self._c._get(f"/cosmos/gov/v1beta1/proposals/{proposal_id}")
        return Proposal.from_data(res.get("proposal"))

    # keep it private
    async def __search_proposal(self, proposal_id: int, action: str, height: int):
        params = [
            ("events", f"message.action='{action}'"),
            ("events", f"submit_proposal.proposal_id={proposal_id}"),
            ("events", f"tx.height={height}")
        ]
        return await self._c._search(params)

    # FIXME: no height.. untested
    async def proposer(self, proposal_id: int) -> str:
        """Fetches the proposer of a proposal.

        Args:
            proposal_id (int): proposal ID

        Returns:
            str: proposal's proposer
        """

        raise NotImplementedError

        # FIXME: height 1 is just filler
        res = await self.__search_proposal(proposal_id,"/cosmos.gov.v1beta1.MsgSubmitProposal", 1)
        return res["proposer"]

    # FIXME: no height.. untested
    async def deposits(self, proposal_id: int):
        """Fetches the deposit information about a proposal.

        Args:
            proposal_id (int): proposal ID
        """

        raise NotImplementedError

        proposal = self.proposal(proposal_id)

        status = proposal.status
        if status == ProposalStatus.PROPOSAL_STATUS_DEPOSIT_PERIOD.name \
                or status == ProposalStatus.PROPOSAL_STATUS_VOTING_PERIOD.name:
            deposits = self._c._get(f"/cosmos/gov/v1beta1/proposals/{proposal_id}/deposits")
            return (Deposit.from_data(d) for d in deposits)

        # FIXME: height 1 is just filler
        depositTxs = self.__search_proposal(
            proposal_id, "/cosmos.gov.v1beta1.MsgDeposit", 1
        )
        return ( Deposit.from_data(d) for d in depositTxs)

    # TODO: col5
    async def votes(self, proposal_id: int):
        """Fetches the votes for a proposal.

        Args:
            proposal_id (int): proposal ID
        """

        raise NotImplementedError

        return await self._c._get(f"/gov/proposals/{proposal_id}/votes")

    async def tally(self, proposal_id: int):
        """Fetches the tally for a proposal.

        Args:
            proposal_id (int): proposal ID
        """
        res = await self._c._get(f"/cosmos/gov/v1beta1/proposals/{proposal_id}/tally")
        return res.get("tally")

    async def deposit_parameters(self) -> dict:
        """Fetches the Gov module's deposit parameters.

        Returns:
            dict: deposit parameters
        """
        result = await self._c._get("/cosmos/gov/v1beta1/params/deposit")
        params = result.get("deposit_params")
        return {
            "max_deposit_period": params["max_deposit_period"],
            "min_deposit": Coins.from_data(params["min_deposit"])
        }

    async def voting_parameters(self) -> dict:
        """Fetches the Gov module's voting parameters.

        Returns:
            dict: voting parameters
        """
        result = await self._c._get("/cosmos/gov/v1beta1/params/voting")
        return result.get("voting_params")

    async def tally_parameters(self) -> dict:
        """Fetches the Gov module's tally parameters.

        Returns:
            dict: tally parameters
        """
        result = await self._c._get("/cosmos/gov/v1beta1/params/tallying")
        params = result.get("tally_params")
        return {
            "quorum": Dec(params["quorum"]),
            "threshold": Dec(params["threshold"]),
            "veto_threshold": Dec(params["veto_threshold"])
        }

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
