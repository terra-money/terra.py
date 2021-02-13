"""Distribution module governance proposal types."""

from __future__ import annotations

import attr

from terra_sdk.core import AccAddress, Coins
from terra_sdk.core.gov import Content

__all__ = ["CommunityPoolSpendProposal"]


@attr.s
class CommunityPoolSpendProposal(Content):
    """Proposal for allocating funds from the community pool to an address.

    Args:
        title: proposal title
        description: proposal description
        recipient: designated recipient of funds if proposal passes
        amount (Coins): amount to spend from community pool
    """

    type = "distribution/CommunityPoolSpendProposal"
    """"""

    title: str = attr.ib()
    description: str = attr.ib()
    recipient: AccAddress = attr.ib()
    amount: Coins = attr.ib(converter=Coins)

    @classmethod
    def from_data(cls, data: dict) -> CommunityPoolSpendProposal:
        data = data["value"]
        return cls(
            title=data["title"],
            description=data["description"],
            recipient=data["recipient"],
            amount=Coins.from_data(data["amount"]),
        )
