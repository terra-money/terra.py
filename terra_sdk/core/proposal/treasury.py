from __future__ import annotations

from dataclasses import dataclass

from terra_sdk.core import Dec
from terra_sdk.core.proposal import Content
from terra_sdk.util.validation import Schemas as S

__all__ = ["TaxRateUpdateProposal"]


@dataclass
class TaxRateUpdateProposal(Content):

    type = "treasury/TaxRateUpdateProposal"


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
