"""Params module governance proposal types."""

from __future__ import annotations

from typing import List

import attr
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
        return {
            "subspace": self.subspace,
            "key": self.key,
            "value": self.value
        }

    @classmethod
    def from_data(cls, data: dict) -> ParamChange:
        return cls(subspace=data["subspace"], key=data["key"], value=data["value"])

    def to_proto(self) -> ParamChange_pb:
        return ParamChange_pb(subspace=self.subspace, key=self.key, value=self.value)


@attr.s
class ParameterChangeProposal(JSONSerializable):
    """Proposal to alter the blockchain parameters. Changes would be effective
    as soon as the proposal is passed.

    Args:
        title: proposal title
        description: proposal description
        change (List[ParamChange]): list of parameter changes
    """

    type_amino = "params/ParameterChangeProposal"
    """"""
    type_url = "/cosmos.params.v1beta1.ParameterChangeProposal"
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
                "changes": [change.to_amino() for change in self.changes]
            }
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
            changes=self.changes.to_proto(),
        )
