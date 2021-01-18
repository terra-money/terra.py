from __future__ import annotations
from dataclasses import dataclass

import attr
from terra_sdk.util.base import BaseMsg


__all__ = ["MsgSubmitProposal", "MsgDeposit", "MsgVote"]


@attr.s
class MsgSubmitProposal(BaseMsg):

    type = "gov/MsgSubmitProposal"
    action = "submit_proposal"

    content: str = attr.ib()
    initial_deposit: Coins = attr.ib()
    proposer: AccAddress = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgSubmitProposal:
        data = data["value"]
        content = p_type.from_data(data["content"])
        return cls(
            content=content,
            initial_deposit=Coins.from_data(data["initial_deposit"]),
            proposer=data["proposer"],
        )


@attr.s
class MsgDeposit(BaseMsg):

    type = "gov/MsgDeposit"
    action = "deposit"

    proposal_id: int = attr.ib()
    depositor: AccAddress = attr.ib()
    amount: Coins = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgDeposit:
        data = data["value"]
        return cls(
            proposal_id=int(data["proposal_id"]),
            depositor=data["depositor"],
            amount=Coins.from_data(data["amount"]),
        )


@dataclass
class MsgVote(BaseMsg):

    type = "gov/MsgVote"
    action = "vote"

    EMPTY = "Empty"
    YES = "Yes"
    ABSTAIN = "Abstain"
    NO = "No"
    NO_WITH_VETO = "NoWithVeto"

    proposal_id: int = attr.ib()
    voter: AccAddress = attr.ib()
    option: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgVote:
        data = data["value"]
        return cls(
            proposal_id=int(data["proposal_id"]),
            voter=data["voter"],
            option=data["option"],
        )
