"""ibc client module data objects."""
from __future__ import annotations

import attr
from terra_proto.ibc.core.client.v1 import Height as Height_pb

from terra_sdk.util.json import JSONSerializable

__all__ = ["Height"]


@attr.s
class Height(JSONSerializable):
    revision_number: int = attr.ib(converter=int)
    revision_height: int = attr.ib(converter=int)

    def to_amino(self) -> dict:
        return {
            "revision_number": self.revision_number,
            "revision_height": self.revision_height
        }

    @classmethod
    def from_data(cls, data: dict) -> Height:
        return cls(
            revision_number=data["revision_number"],
            revision_height=data["revision_height"],
        )

    def to_proto(self) -> Height_pb:
        return Height_pb(
            revision_number=self.revision_number, revision_height=self.revision_height
        )
