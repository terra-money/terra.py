from __future__ import annotations

from dataclasses import dataclass

from terra_sdk.core import Dec
from terra_sdk.core.proposal import Content
from terra_sdk.util.validation import Schemas as S

__all__ = ["TaxRateUpdateProposal"]


@dataclass
class TaxRateUpdateProposal(Content):

    type = "treasury/TaxRateUpdateProposal"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^treasury/TaxRateUpdateProposal\Z"),
        value=S.OBJECT(title=S.STRING, description=S.STRING, tax_rate=Dec.__schema__),
    )

    title: str
    description: str
    tax_rate: Dec

    @classmethod
    def from_data(cls, data: dict) -> TaxRateUpdateProposal:
        data = data["value"]
        return cls(
            title=data["title"],
            description=data["description"],
            tax_rate=Dec(data["tax_rate"]),
        )


@dataclass
class RewardWeightUpdateProposal(Content):

    type = "treasury/RewardWeightUpdateProposal"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^treasury/RewardWeightUpdateProposal\Z"),
        value=S.OBJECT(
            title=S.STRING, description=S.STRING, reward_weight=Dec.__schema__
        ),
    )

    title: str
    description: str
    reward_weight: Dec

    @classmethod
    def from_data(cls, data: dict) -> RewardWeightUpdateProposal:
        data = data["value"]
        return cls(
            title=data["title"],
            description=data["description"],
            reward_weight=Dec(data["reward_weight"]),
        )
