from __future__ import annotations

import base64
from abc import ABC, abstractmethod
from typing import List, Optional, Union

import attr
from betterproto.lib.google.protobuf import Any as Any_pb
from terra_proto.cosmos.crypto.ed25519 import PubKey as ValConsPubKey_pb
from terra_proto.cosmos.crypto.multisig import LegacyAminoPubKey as LegacyAminoPubKey_pb
from terra_proto.cosmos.crypto.secp256k1 import PubKey as SimplePubKey_pb

from terra_sdk.util.json import JSONSerializable

__all__ = ["PublicKey", "SimplePublicKey", "ValConsPubKey", "LegacyAminoPubKey"]


class PublicKey(JSONSerializable, ABC):
    """Data object holding the public key component of an account or signature."""

    @abstractmethod
    def get_type(self) -> str:
        return self.type_url

    @classmethod
    def from_proto(cls, proto: Any_pb):
        type_url = proto.type_url
        if type_url == SimplePublicKey.type_url:
            return SimplePublicKey.from_proto(proto)
        elif type_url == ValConsPubKey.type_url:
            return ValConsPubKey.from_proto(proto)
        elif type_url == LegacyAminoPubKey.type_url:
            return LegacyAminoPubKey.from_proto(proto)
        raise TypeError(f"could not marshal PublicKey: type is incorrect")

    @classmethod
    def from_data(cls, data: dict):
        type_url = data["@type"]
        if type_url == SimplePublicKey.type_url:
            return SimplePublicKey.from_data(data)
        elif type_url == ValConsPubKey.type_url:
            return ValConsPubKey.from_data(data)
        elif type_url == LegacyAminoPubKey.type_url:
            return LegacyAminoPubKey.from_data(data)
        raise TypeError(f"could not unmarshal PublicKey: type is incorrect")

    @abstractmethod
    def pack_any(self) -> Any_pb:
        raise NotImplementedError


@attr.s
class SimplePublicKey(PublicKey):
    """Data object holding the SIMPLE public key component of an account or signature."""

    type_amino = "tendermint/PubKeySecp256k1"
    """"""

    type_url = "/cosmos.crypto.secp256k1.PubKey"
    """Normal signature public key type."""

    key: str = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": self.key
        }

    def to_data(self) -> dict:
        return {"key": self.key}

    @classmethod
    def from_data(cls, data: dict) -> SimplePublicKey:
        return cls(key=data["key"])

    def to_proto(self) -> SimplePubKey_pb:
        return SimplePubKey_pb(key=self.key)

    def get_type(self) -> str:
        return self.type_url

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))


@attr.s
class ValConsPubKey(PublicKey):
    """Data object holding the public key component of an validator's account or signature."""

    type_amino = "tendermint/PubKeyEd25519"
    """"""

    type_url = "/cosmos.crypto.ed25519.PubKey"
    """an ed25519 tendermint public key type."""

    key: str = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": self.key
        }

    def to_data(self) -> dict:
        return {"key": self.key}

    @classmethod
    def from_data(cls, data: dict) -> ValConsPubKey:
        return cls(key=data["key"])

    def get_type(self) -> str:
        return self.type_url

    def to_proto(self) -> ValConsPubKey_pb:
        return ValConsPubKey_pb(key=base64.b64encode(self.key))

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))


# FIXME: NOT TESTED
class LegacyAminoPubKey(PublicKey):
    """Data object holding the Legacy Amino-typed public key component of an account or signature."""

    type_amino = "tendermint/PubKeyMultisigThreshold"
    """"""

    type_url = "/cosmos.crypto.multisig.LegacyAminoPubKey"
    """Multisig public key type."""

    threshold: int = attr.ib(converter=int)
    public_keys: List[bytes] = attr.ib(factory=List)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "threshold": str(self.threshold),
                "pubkeys": [pubkey.to_amino() for pubkey in self.public_keys]
            }
        }

    def to_data(self) -> dict:
        return {"threshold": self.threshold, "public_keys": self.public_keys}

    @classmethod
    def from_data(cls, data: dict) -> LegacyAminoPubKey:
        return cls(threshold=data["threshold"], public_keys=data["public_keys"])

    def get_type(self) -> str:
        return self.type_url

    def to_proto(self) -> LegacyAminoPubKey_pb:
        return LegacyAminoPubKey_pb(
            threshold=self.threshold, public_keys=self.public_keys
        )

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))
