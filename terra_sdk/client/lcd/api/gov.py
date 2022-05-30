from typing import List, Optional, Tuple

from terra_sdk.core import Coins, Dec
from terra_sdk.core.deposit import Deposit
from terra_sdk.core.gov import Proposal, ProposalStatus, WeightedVoteOption
from terra_sdk.core.gov.data import Vote

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncGovAPI", "GovAPI", "ProposalStatus"]

from ..params import APIParams


class AsyncGovAPI(BaseAsyncAPI):
    async def proposals(
        self, options: dict = {}, params: Optional[APIParams] = None
    ) -> [List[Proposal], dict]:
        """Fetches all proposals.
        Args:
            options (dict, optional): dictionary containing options. Defaults to {}. you can use one or more below:
                {
                    "proposal_status": terra_sdk.core.gov.ProposalStatus (int)
                    "voter": voter address (str),
                    "depositor": depositor address(str)
                }
                example) {"proposal_status":1, "depositor":"terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp"}

            params (APIParams, optional): additional params for the API like pagination

        Returns:
            List[Proposal]: proposals
        """
        if params is not None:
            options.update(params.to_dict())
        res = await self._c._get("/cosmos/gov/v1beta1/proposals", options)
        return [Proposal.from_data(d) for d in res.get("proposals")], res.get(
            "pagination"
        )

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
    async def __search_submit_proposal(self, proposal_id: int):
        params = [
            ("message.action", "/cosmos.gov.v1beta1.MsgSubmitProposal"),
            ("submit_proposal.proposal_id", proposal_id),
        ]

        res = await self._c._search(params)
        txs = res.get("txs")
        if txs is None or len(txs) <= 0:
            raise Exception("failed to find submit proposal")
        return txs[0]

    # keep it private
    async def __search_deposits(
        self, proposal_id: int, params: Optional[APIParams] = None
    ):
        events = [
            ("message.action", "/cosmos.gov.v1beta1.MsgDeposit"),
            ("proposal_deposit.proposal_id", proposal_id),
        ]
        if params is not None:
            d = params.to_dict()
            for i in d.keys():
                events.append((i, d.get(i)))
        res = await self._c._search(events)
        txs = res.get("txs")
        if txs is None or len(txs) <= 0:
            raise Exception("failed to find deposit txs")
        return txs, res.get("pagination")

    # keep it private
    async def __search_votes(
        self, proposal_id: int, action: str, params: Optional[APIParams] = None
    ):
        events = [
            ("message.action", "/cosmos.gov.v1beta1.MsgVote"),
            ("proposal_vote.proposal_id", proposal_id),
        ]
        if params is not None:
            d = params.to_dict()
            for i in d.keys():
                events.append((i, d.get(i)))

        res = await self._c._search(events)
        txs = res.get("txs")
        if txs is None or len(txs) <= 0:
            raise Exception("failed to find vote txs")
        return txs, res.get("pagination")

    async def proposer(self, proposal_id: int) -> str:
        """Fetches the proposer of a proposal.

        Args:
            proposal_id (int): proposal ID

        Returns:
            str: proposal's proposer, None if proposal is not exist
        """

        res = await self.__search_submit_proposal(proposal_id)
        msgs = res["body"]["messages"]
        for msg in msgs:
            if msg.get("@type") == "/cosmos.gov.v1beta1.MsgSubmitProposal":
                return msg["proposer"]
        return None

    async def deposits(self, proposal_id: int, params: Optional[APIParams] = None):
        """Fetches the deposit information about a proposal.

        Args:
            proposal_id (int): proposal ID
            params (APIParams, optional): additional params for the API like pagination
        """

        proposal = self.proposal(proposal_id)

        status = proposal.status
        if (
            status == ProposalStatus.PROPOSAL_STATUS_DEPOSIT_PERIOD.name
            or status == ProposalStatus.PROPOSAL_STATUS_VOTING_PERIOD.name
        ):
            res = await self._c._get(
                f"/cosmos/gov/v1beta1/proposals/{proposal_id}/deposits", params
            )
            return [Deposit.from_data(d) for d in res.get("deposits")]

        res, pagination = await self.__search_deposits(proposal_id, params)
        deposits = []
        for tx in res:
            for msg in tx.get("body").get("messages"):
                if msg.get("@type") == "/cosmos.gov.v1beta1.MsgDeposit":
                    deposits.append(Deposit.from_data(msg))
        return deposits, pagination

    async def votes(self, proposal_id: int, params: Optional[APIParams] = None):
        """Fetches the votes for a proposal.

        Args:
            proposal_id (int): proposal ID
            params (APIParams, optional): additional params for the API like pagination
        """

        proposal = self.proposal(proposal_id)
        if proposal.status == ProposalStatus.PROPOSAL_STATUS_DEPOSIT_PERIOD:
            res = await self._c._get(
                f"/cosmos/gov/v1beta1/proposals/{proposal_id}/votes", params
            )
            return res.get("votes"), res.get("pagination")

        res, pagination = await self.__search_votes(proposal_id, params)
        votes = []
        for tx in res:
            for msg in tx.get("body").get("messages"):
                if (
                    msg.get("@type") == "/cosmos.gov.v1beta1.MsgVote"
                    and msg.get("proposal_id") == proposal_id
                ):
                    votes.append(WeightedVoteOption(msg.get("option"), 1))
                elif (
                    msg.get("@type") == "/cosmos.gov.v1beta1.MsgVoteWeighted"
                    and msg.get("proposal_id") == proposal_id
                ):
                    votes.append(
                        Vote(
                            proposal_id=proposal_id,
                            voter=msg.get("voter"),
                            options=msg.get("options"),
                        )
                    )
        return votes, pagination

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
            "min_deposit": Coins.from_data(params["min_deposit"]),
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
            "veto_threshold": Dec(params["veto_threshold"]),
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
    def proposals(self, params: Optional[APIParams] = None) -> Tuple[List[Proposal], dict]:
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
    def deposits(self, proposal_id: int, params: Optional[APIParams] = None):
        pass

    deposits.__doc__ = AsyncGovAPI.deposits.__doc__

    @sync_bind(AsyncGovAPI.votes)
    def votes(self, proposal_id: int, params: Optional[APIParams] = None):
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
