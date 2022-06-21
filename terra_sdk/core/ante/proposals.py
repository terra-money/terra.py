"""Ante module governance proposal types."""

from __future__ import annotations

import attr
from betterproto.lib.google.protobuf import Any as Any_pb
from terra_proto.terra.ante.v2 import (
    MinimumCommissionUpdateProposal as MinimumCommissionUpdateProposal_pb,
)

from terra_sdk.core import AccAddress, Coins
from terra_sdk.util.json import JSONSerializable

__all__ = ["MinimumCommissionUpdateProposal"]


@attr.s
class MinimumCommissionUpdateProposal(JSONSerializable):
    """Proposal for updating validator's minimum commission.

    Args:
        title: proposal title
        description: proposal description
        minimum_commission: validator's minimum commission
    """

    """"""
    type_url = "/terra.ante.v2.MinimumCommissionUpdateProposal"
    """"""
    prototype = MinimumCommissionUpdateProposal_pb
    """"""

    title: str = attr.ib()
    description: str = attr.ib()
    minimum_commission: str = attr.ib()

    # Amino not supported
    def to_amino(self) -> dict:
        pass

    @classmethod
    def from_data(cls, data: dict) -> MinimumCommissionUpdateProposal:
        return cls(
            title=data["title"],
            description=data["description"],
            minimum_commission=data["minimum_commission"],
        )

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "title": self.title,
            "description": self.description,
            "minimum_commission": self.minimum_commission,
        }

    def to_proto(self) -> MinimumCommissionUpdateProposal_pb:
        return MinimumCommissionUpdateProposal_pb(
            title=self.title,
            description=self.description,
            minimum_commission=self.minimum_commission,
        )

    @classmethod
    def from_proto(
        cls, proto: MinimumCommissionUpdateProposal_pb
    ) -> MinimumCommissionUpdateProposal:
        return cls(
            title=proto.title,
            description=proto.description,
            minimum_commission=proto.minimum_commission,
        )

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))
