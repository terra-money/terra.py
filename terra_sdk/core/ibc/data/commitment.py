"""ibc commitment module data objects."""
from __future__ import annotations

import base64

import attr
from terra_proto.ibc.core.commitment.v1 import MerklePrefix as MerklePrefix_pb
from terra_proto.ibc.core.commitment.v1 import MerkleRoot as MerkleRoot_pb

from terra_sdk.util.json import JSONSerializable

__all__ = ["MerkleRoot", "MerklePrefix"]


@attr.s
class MerkleRoot(JSONSerializable):
    hash: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> MerkleRoot:
        return cls(hash=(data["hash"]))

    def to_proto(self) -> MerkleRoot_pb:
        return MerkleRoot_pb(hash=base64.b64decode(self.hash))

    @classmethod
    def from_proto(cls, proto: MerkleRoot_pb) -> MerkleRoot:
        return cls(hash=base64.b64encode(proto.hash).decode())


@attr.s
class MerklePrefix(JSONSerializable):
    key_prefix: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> MerklePrefix:
        return cls(key_prefix=data["key_prefix"])

    def to_proto(self) -> MerklePrefix_pb:
        return MerklePrefix_pb(key_prefix=base64.b64decode(self.key_prefix))

    @classmethod
    def from_proto(cls, proto: MerklePrefix_pb) -> MerklePrefix:
        return cls(key_prefix=base64.b64encode(proto.key_prefix).decode())
