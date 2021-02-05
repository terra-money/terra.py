from __future__ import annotations

import attr

from terra_sdk.core import Dec
from terra_sdk.core.gov import Content

__all__ = ["TaxRateUpdateProposal", "RewardWeightUpdateProposal"]


@attr.s
class TaxRateUpdateProposal(Content):

    type = "treasury/TaxRateUpdateProposal"

    title: str = attr.ib()
    description: str = attr.ib()
    tax_rate: Dec = attr.ib(converter=Dec)

    @classmethod
    def from_data(cls, data: dict) -> TaxRateUpdateProposal:
        data = data["value"]
        return cls(
            title=data["title"],
            description=data["description"],
            tax_rate=data["tax_rate"],
        )


@attr.s
class RewardWeightUpdateProposal(Content):

    type = "treasury/RewardWeightUpdateProposal"

    title: str = attr.ib()
    description: str = attr.ib()
    reward_weight: Dec = attr.ib(converter=Dec)

    @classmethod
    def from_data(cls, data: dict) -> RewardWeightUpdateProposal:
        data = data["value"]
        return cls(
            title=data["title"],
            description=data["description"],
            reward_weight=data["reward_weight"],
        )
