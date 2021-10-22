from __future__ import annotations

from abc import ABC
from typing import Optional, Union, List

import attr

from terra_sdk.util.json import JSONSerializable
from terra_proto.cosmos.crypto.secp256k1 import PubKey as SimplePubKey_pb
from terra_proto.cosmos.crypto.ed25519 import PubKey as ValConsPubKey_pb
from terra_proto.cosmos.crypto.multisig import LegacyAminoPubKey as LegacyAminoPubKey_pb
from betterproto.lib.google.protobuf import Any

__all__ = ["PublicKey", "SimplePublicKey", "ValConsPubKey"]


class PublicKey(JSONSerializable, ABC):
    """Data object holding the public key component of an account or signature."""

    @classmethod
    def from_proto(cls, proto: Any):
        type_url = proto.type_url
        if type_url == SimplePublicKey.type_url:
            return SimplePublicKey.from_proto(proto)
        elif type_url == ValConsPubKey.type_url:
            return ValConsPubKey.from_proto(proto)
        # elif type_url == LegacyAminoPubKey.type_url:
        #    return LegacyAminoPubKey.from_proto(proto)
        raise TypeError(f"could not marshal PublicKey: type is incorrect")

    @classmethod
    def from_data(cls, data: dict):
        type_url = data["@type"]
        if type_url == SimplePublicKey.type_url:
            return SimplePublicKey.from_data(data)
        elif type_url == ValConsPubKey.type_url:
            return ValConsPubKey.from_data(data)
        # elif type_url == LegacyAminoPubKey.type_url:
        #    return LegacyAminoPubKey.from_data(data)
        raise TypeError(f"could not unmarshal PublicKey: type is incorrect")


@attr.s
class SimplePublicKey(PublicKey):
    """Data object holding the SIMPLE public key component of an account or signature."""

    type_url = "/cosmos.crypto.secp256k1.PubKey"
    """Normal signature public key type."""

    key: bytes = attr.ib()

    def to_data(self) -> dict:
        return {
            "key": self.key
        }

    def to_proto(self) -> SimplePubKey_pb:
        proto = SimplePubKey_pb()
        proto.key = self.key
        return self

    @classmethod
    def from_data(cls, data: dict) -> SimplePublicKey:
        return cls(
            key=data["key"]
        )

    @classmethod
    def from_proto(cls, proto: SimplePubKey_pb) -> SimplePublicKey:
        return cls(key=proto.key)


@attr.s
class ValConsPubKey(PublicKey):
    """Data object holding the public key component of an validator's account or signature."""

    type_url = "/cosmos.crypto.ed25519.PubKey"
    """an ed25519 tendermint public key type."""

    key: bytes = attr.ib()

    def to_data(self) -> dict:
        return {
            "key": self.key
        }

    def to_proto(self) -> ValConsPubKey_pb:
        proto = ValConsPubKey_pb()
        proto.key = self.key
        return self

    @classmethod
    def from_data(cls, data: dict) -> ValConsPubKey:
        return cls(
            key=data["key"]
        )

    @classmethod
    def from_proto(cls, proto: ValConsPubKey_pb) -> ValConsPubKey:
        return cls(key=proto.key)


# NOT TESTED
@attr.s
class LegacyAminoPubKey(PublicKey):
    """Data object holding the Legacy Amino-typed public key component of an account or signature."""

    type_url = "/cosmos.crypto.multisig.LegacyAminoPubKey"
    """Multisig public key type."""

    threshold: int = attr.ib(converter=int)
    public_keys: List[bytes] = attr.ib(factory=List)

    def to_data(self) -> dict:
        return {
            "threshold": self.threshold,
            "public_keys": self.public_keys
        }

    def to_proto(self) -> LegacyAminoPubKey_pb:
        return LegacyAminoPubKey_pb().from_dict(self.to_data())

    @classmethod
    def from_data(cls, data: dict) -> LegacyAminoPubKey:
        return cls(
            threshold=data["threshold"],
            public_keys=data["public_keys"]
        )

    @classmethod
    def from_proto(cls, proto: LegacyAminoPubKey_pb) -> LegacyAminoPubKey:
        return cls(
            threshold=proto.threshold,
            public_keys=[Any.parse(pubkey) for pubkey in proto.public_keys]
        )
