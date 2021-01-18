from __future__ import annotations

from dataclasses import dataclass
from typing import Type

from terra_sdk.core import AccAddress, Coins
from terra_sdk.core.msg import StdMsg
from terra_sdk.core.proposal import PROPOSAL_TYPES, Content
from terra_sdk.util.validation import Schemas as S
from terra_sdk.util.validation import validate_acc_address

__all__ = ["MsgSubmitProposal", "MsgDeposit", "MsgVote"]


@dataclass
class MsgSubmitProposal(StdMsg):

    type = "gov/MsgSubmitProposal"
    action = "submit_proposal"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^gov/MsgSubmitProposal\Z"),
        value=S.OBJECT(
            content=S.ANY(*(pt.__schema__ for pt in PROPOSAL_TYPES.values())),
            initial_deposit=Coins.__schema__,
            proposer=S.ACC_ADDRESS,
        ),
    )

    content: Type[Content]
    initial_deposit: Coins
    proposer: AccAddress

    def __post_init__(self):
        self.proposer = validate_acc_address(self.proposer)
        self.initial_deposit = Coins(self.initial_deposit)

    @classmethod
    def from_data(cls, data: dict) -> MsgSubmitProposal:
        data = data["value"]
        p_type = PROPOSAL_TYPES[data["content"]["type"]]
        content = p_type.from_data(data["content"])
        return cls(
            content=content,
            initial_deposit=Coins.from_data(data["initial_deposit"]),
            proposer=data["proposer"],
        )


@dataclass
class MsgDeposit(StdMsg):

    type = "gov/MsgDeposit"
    action = "deposit"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^gov/MsgDeposit\Z"),
        value=S.OBJECT(
            proposal_id=S.STRING_INTEGER,
            depositor=S.ACC_ADDRESS,
            amount=Coins.__schema__,
        ),
    )

    proposal_id: int
    depositor: AccAddress
    amount: Coins

    def __post_init__(self):
        self.depositor = validate_acc_address(self.depositor)
        self.amount = Coins(self.amount)

    def msg_value(self) -> dict:
        d = dict(self.__dict__)
        d["proposal_id"] = str(self.proposal_id)
        return d

    @classmethod
    def from_data(cls, data: dict) -> MsgDeposit:
        data = data["value"]
        return cls(
            proposal_id=int(data["proposal_id"]),
            depositor=data["depositor"],
            amount=Coins.from_data(data["amount"]),
        )


@dataclass
class MsgVote(StdMsg):

    type = "gov/MsgVote"
    action = "vote"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^gov/MsgVote\Z"),
        value=S.OBJECT(
            proposal_id=S.STRING_INTEGER,
            voter=S.ACC_ADDRESS,
            option=S.ONE(S.STRING, S.INTEGER),  # signing is different
        ),
    )

    EMPTY = "Empty"
    YES = "Yes"
    ABSTAIN = "Abstain"
    NO = "No"
    NO_WITH_VETO = "NoWithVeto"

    proposal_id: int
    voter: AccAddress
    option: str

    def __post_init__(self):
        self.voter = validate_acc_address(self.voter)

    def msg_value(self) -> dict:
        d = dict(self.__dict__)
        d["proposal_id"] = str(self.proposal_id)
        return d

    @classmethod
    def from_data(cls, data: dict) -> MsgVote:
        data = data["value"]
        return cls(
            proposal_id=int(data["proposal_id"]),
            voter=data["voter"],
            option=data["option"],
        )
