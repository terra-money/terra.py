"""Distribution module governance proposal types."""

from __future__ import annotations

import attr
from betterproto.lib.google.protobuf import Any as Any_pb
from terra_proto.cosmos.distribution.v1beta1 import (
    CommunityPoolSpendProposal as CommunityPoolSpendProposal_pb,
)

from terra_sdk.core import AccAddress, Coins
from terra_sdk.util.json import JSONSerializable

__all__ = ["CommunityPoolSpendProposal"]


@attr.s
class CommunityPoolSpendProposal(JSONSerializable):
    """Proposal for allocating funds from the community pool to an address.

    Args:
        title: proposal title
        description: proposal description
        recipient: designated recipient of funds if proposal passes
        amount (Coins): amount to spend from community pool
    """

    type_amino = "cosmos-sdk/CommunityPoolSpendProposal"
    """"""
    type_url = "/cosmos.distribution.v1beta1.CommunityPoolSpendProposal"
    """"""
    prototype = CommunityPoolSpendProposal_pb
    """"""

    title: str = attr.ib()
    description: str = attr.ib()
    recipient: AccAddress = attr.ib()
    amount: Coins = attr.ib(converter=Coins)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "title": self.title,
                "description": self.description,
                "recipient": self.recipient,
                "amount": self.amount.to_amino(),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> CommunityPoolSpendProposal:
        return cls(
            title=data["title"],
            description=data["description"],
            recipient=data["recipient"],
            amount=Coins.from_data(data["amount"]),
        )

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "title": self.title,
            "description": self.description,
            "recipient": self.recipient,
            "amount": self.amount.to_data(),
        }

    def to_proto(self) -> CommunityPoolSpendProposal_pb:
        return CommunityPoolSpendProposal_pb(
            title=self.title,
            description=self.description,
            recipient=self.recipient,
            amount=self.amount.to_proto(),
        )

    @classmethod
    def from_proto(
        cls, proto: CommunityPoolSpendProposal_pb
    ) -> CommunityPoolSpendProposal:
        return cls(
            title=proto.title,
            description=proto.description,
            recipient=proto.recipient,
            amount=Coins.from_proto(proto.amount),
        )

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))
