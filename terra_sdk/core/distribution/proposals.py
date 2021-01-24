from __future__ import annotations

import attr

__all__ = ["CommunityPoolSpendProposal"]


@attr.s
class CommunityPoolSpendProposal:

    type = "distribution/CommunityPoolSpendProposal"

    title: str
    description: str
    recipient: AccAddress
    amount: Coins

    @classmethod
    def from_data(cls, data: dict) -> CommunityPoolSpendProposal:
        data = data["value"]
        return cls(
            title=data["title"],
            description=data["description"],
            recipient=data["recipient"],
            amount=Coins.from_data(data["amount"]),
        )
