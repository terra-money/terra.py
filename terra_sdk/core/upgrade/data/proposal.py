"""Upgrade module data objects."""

from __future__ import annotations

__all__ = ["SoftwareUpgradeProposal", "CancelSoftwareUpgradeProposal"]

from typing import Optional

import attr
from betterproto.lib.google.protobuf import Any as Any_pb
from terra_proto.cosmos.upgrade.v1beta1 import (
    CancelSoftwareUpgradeProposal as CancelSoftwareUpgradeProposal_pb,
)
from terra_proto.cosmos.upgrade.v1beta1 import (
    SoftwareUpgradeProposal as SoftwareUpgradeProposal_pb,
)

from terra_sdk.core.upgrade.plan import Plan
from terra_sdk.util.json import JSONSerializable


@attr.s
class SoftwareUpgradeProposal(JSONSerializable):
    title: str = attr.ib()
    description: str = attr.ib()
    plan: Optional[Plan] = attr.ib()

    type_amino = "cosmos-sdk/SoftwareUpgradeProposal"
    """"""
    type_url = "/cosmos.upgrade.v1beta1.SoftwareUpgradeProposal"
    """"""
    prototype = SoftwareUpgradeProposal_pb
    """"""

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "title": self.title,
                "description": self.description,
                "plan": self.plan.to_amino() if self.plan else None,
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> SoftwareUpgradeProposal:
        return cls(
            title=data["title"],
            description=data["description"],
            plan=Plan.from_data(data["plan"]) if data.get("plan") else None,
        )

    def to_proto(self) -> SoftwareUpgradeProposal_pb:
        return SoftwareUpgradeProposal_pb(
            title=self.title,
            description=self.description,
            plan=(self.plan.to_proto() if self.plan else None),
        )

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))

    @classmethod
    def from_proto(cls, proto: SoftwareUpgradeProposal_pb) -> SoftwareUpgradeProposal:
        return cls(
            title=proto.title,
            description=proto.description,
            plan=Plan.from_proto(proto.plan) if proto.plan else None,
        )


@attr.s
class CancelSoftwareUpgradeProposal(JSONSerializable):
    title: str = attr.ib()
    description: str = attr.ib()

    type_amino = "cosmos-sdk/CancelSoftwareUpgradeProposal"
    """"""
    type_url = "/cosmos.upgrade.v1beta1.CancelSoftwareUpgradeProposal"
    """"""
    prototype = CancelSoftwareUpgradeProposal_pb
    """"""

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "title": self.title,
                "description": self.description,
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> CancelSoftwareUpgradeProposal:
        return cls(title=data["title"], description=data["description"])

    def to_proto(self) -> CancelSoftwareUpgradeProposal_pb:
        return CancelSoftwareUpgradeProposal_pb(
            title=self.title, description=self.description
        )

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))

    @classmethod
    def from_proto(
        cls, proto: CancelSoftwareUpgradeProposal_pb
    ) -> CancelSoftwareUpgradeProposal:
        return cls(title=proto.title, description=proto.description)
