from __future__ import annotations

import attr

__all__ = ["TaxRateUpdateProposal"]


@attr.s
class TaxRateUpdateProposal(Content):

    type = "treasury/TaxRateUpdateProposal"

    title: str    = attr.ib()
    description: str = attr.ib()
    tax_rate: Dec = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> TaxRateUpdateProposal:
        data = data["value"]
        return cls(
            title=data["title"],
            description=data["description"],
            tax_rate=Dec(data["tax_rate"]),
        )


@attr.s
class RewardWeightUpdateProposal(Content):

    type = "treasury/RewardWeightUpdateProposal"

    title: str         = attr.ib()
    description: str   = attr.ib()
    reward_weight: Dec = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> RewardWeightUpdateProposal:
        data = data["value"]
        return cls(
            title=data["title"],
            description=data["description"],
            reward_weight=Dec(data["reward_weight"]),
        )
