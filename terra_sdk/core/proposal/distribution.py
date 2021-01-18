from __future__ import annotations

from dataclasses import dataclass

from terra_sdk.core import AccAddress, Coins
from terra_sdk.core.proposal import Content
from terra_sdk.util.validation import Schemas as S

__all__ = ["CommunityPoolSpendProposal"]


@dataclass
class CommunityPoolSpendProposal(Content):

    type = "distribution/CommunityPoolSpendProposal"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^distribution/CommunityPoolSpendProposal\Z"),
        value=S.OBJECT(
            title=S.STRING,
            description=S.STRING,
            recipient=S.ACC_ADDRESS,
            amount=Coins.__schema__,
        ),
    )

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
