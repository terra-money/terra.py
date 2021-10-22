from .data import Content, Proposal
from .msgs import MsgDeposit, MsgSubmitProposal, MsgVote
from .proposals import TextProposal

from terra_proto.cosmos.gov.v1beta1 import ProposalStatus

__all__ = [
    "Content",
    "MsgDeposit",
    "MsgSubmitProposal",
    "MsgVote",
    "Proposal",
    "TextProposal",
    "ProposalStatus"
]
