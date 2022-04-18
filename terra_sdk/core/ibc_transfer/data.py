"""ibc-trasfer module data objects."""
from __future__ import annotations

import attr
from terra_proto.ibc.applications.transfer.v1 import DenomTrace as DenomTrace_pb

from terra_sdk.util.json import JSONSerializable

__all__ = ["DenomTrace"]


@attr.s
class DenomTrace(JSONSerializable):
    path: str = attr.ib()
    base_denom: str = attr.ib()

    def to_amino(self) -> dict:
        return {"path": self.path, "base_denom": self.base_denom}

    @classmethod
    def from_data(cls, data: dict) -> DenomTrace:
        return cls(path=data["path"], base_denom=data["base_denom"])

    def to_proto(self) -> DenomTrace_pb:
        return DenomTrace_pb(path=self.path, base_denom=self.base_denom)
