"""ibc connection module data objects."""
from __future__ import annotations

from typing import List

import attr
from terra_proto.ibc.core.connection.v1 import Counterparty as Counterparty_pb
from terra_proto.ibc.core.connection.v1 import Version as Version_pb

from terra_sdk.util.json import JSONSerializable

from .commitment import MerklePrefix

__all__ = ["Version", "Counterparty"]


@attr.s
class Version(JSONSerializable):
    identifier: str = attr.ib()
    features: List[str] = attr.ib(converter=list)

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> Version:
        return cls(
            identifier=data["identifier"],
            features=data["features"],
        )

    def to_proto(self) -> Version_pb:
        return Version_pb(identifier=self.identifier, features=self.features)

    @classmethod
    def from_proto(cls, proto: Version_pb) -> Version:
        return cls(identifier=proto.identifier, features=proto.features)


@attr.s
class Counterparty(JSONSerializable):
    client_id: str = attr.ib()
    connection_id: str = attr.ib()
    prefix: MerklePrefix = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> Counterparty:
        return cls(
            client_id=data["client_id"],
            connection_id=data["client_id"],
            prefix=data["prefix"],
        )

    def to_proto(self) -> Counterparty_pb:
        return Counterparty_pb(
            client_id=self.client_id,
            connection_id=self.connection_id,
            prefix=self.prefix.to_proto(),
        )

    @classmethod
    def from_proto(cls, proto: Counterparty_pb) -> Counterparty:
        return cls(
            client_id=proto.client_id,
            connection_id=proto.connection_id,
            prefix=MerklePrefix.from_proto(proto.prefix),
        )
