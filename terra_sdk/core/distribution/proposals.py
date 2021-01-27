from __future__ import annotations

import attr

from terra_sdk.core import Coins

__all__ = ["CommunityPoolSpendProposal"]


@attr.s
class CommunityPoolSpendProposal:

    type = "distribution/CommunityPoolSpendProposal"

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
