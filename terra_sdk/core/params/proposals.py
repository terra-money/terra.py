"""Params module governance proposal types."""

from __future__ import annotations

from typing import List

import attr
from betterproto.lib.google.protobuf import Any as Any_pb
from terra_proto.cosmos.params.v1beta1 import ParamChange as ParamChange_pb
from terra_proto.cosmos.params.v1beta1 import (
    ParameterChangeProposal as ParameterChangeProposal_pb,
)

from terra_sdk.util.json import JSONSerializable

__all__ = ["ParameterChangeProposal", "ParamChange"]


@attr.s
class ParamChange(JSONSerializable):
    subspace: str = attr.ib()
    key: str = attr.ib()
    value: str = attr.ib()

    def to_amino(self) -> dict:
        return {"subspace": self.subspace, "key": self.key, "value": self.value}

    @classmethod
    def from_data(cls, data: dict) -> ParamChange:
        return cls(subspace=data["subspace"], key=data["key"], value=data["value"])

    def to_proto(self) -> ParamChange_pb:
        return ParamChange_pb(subspace=self.subspace, key=self.key, value=self.value)

    def to_data(self) -> dict:
        return {"subspace": self.subspace, "key": self.key, "value": self.value}

    @classmethod
    def from_proto(cls, proto: ParamChange_pb) -> ParamChange:
        return cls(subspace=proto.subspace, key=proto.key, value=proto.value)


@attr.s
class ParameterChangeProposal(JSONSerializable):
    """Proposal to alter the blockchain parameters. Changes would be effective
    as soon as the proposal is passed.

    Args:
        title: proposal title
        description: proposal description
        change (List[ParamChange]): list of parameter changes
    """

    type_amino = "cosmos-sdk/ParameterChangeProposal"
    """"""
    type_url = "/cosmos.params.v1beta1.ParameterChangeProposal"
    """"""
    prototype = ParameterChangeProposal_pb
    """"""

    title: str = attr.ib()
    description: str = attr.ib()
    changes: List[ParamChange] = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "title": self.title,
                "description": self.description,
                "changes": [change.to_amino() for change in self.changes],
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> ParameterChangeProposal:
        return cls(
            title=data["title"],
            description=data["description"],
            changes=[ParamChange.from_data(change) for change in data["changes"]],
        )

    def to_proto(self) -> ParameterChangeProposal_pb:
        return ParameterChangeProposal_pb(
            title=self.title,
            description=self.description,
            changes=[change.to_proto() for change in self.changes],
        )

    def to_data(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "changes": [change.to_data() for change in self.changes],
        }

    @classmethod
    def from_proto(cls, proto: ParameterChangeProposal_pb) -> ParameterChangeProposal:
        return cls(
            title=proto.title,
            description=proto.description,
            changes=[ParamChange.from_proto(change) for change in proto.changes],
        )

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))
