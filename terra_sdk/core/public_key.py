from __future__ import annotations

import base64
import hashlib
from abc import ABC, abstractmethod
from typing import List, Union

import attr
from betterproto.lib.google.protobuf import Any as Any_pb
from terra_proto.cosmos.crypto.ed25519 import PubKey as ValConsPubKey_pb
from terra_proto.cosmos.crypto.multisig import LegacyAminoPubKey as LegacyAminoPubKey_pb
from terra_proto.cosmos.crypto.secp256k1 import PubKey as SimplePubKey_pb

from terra_sdk.util.json import JSONSerializable

from ..util.base import create_demux_unpack_any
from .bech32 import get_bech

BECH32_AMINO_PUBKEY_DATA_PREFIX_SECP256K1 = "eb5ae987" + "21"  # with fixed length 21
BECH32_AMINO_PUBKEY_DATA_PREFIX_ED25519 = "1624de64" + "20"  # with fixed length 20
BECH32_AMINO_PUBKEY_DATA_PREFIX_MULTISIG_THRESHOLD = "22c1f7e2"  # without length


__all__ = [
    "PublicKey",
    "SimplePublicKey",
    "ValConsPubKey",
    "LegacyAminoMultisigPublicKey",
    "address_from_public_key",
    "amino_pubkey_from_public_key",
]


def encode_uvarint(value: Union[int, str]) -> List[int]:
    val = int(str(value))
    if val > 127:
        raise ValueError(
            "Encoding numbers > 127 is not supported here. Please tell those lazy CosmJS maintainers to "
            "port the binary.PutUvarint implementation from the Go standard library and write some "
            "tests."
        )
    return [val]


def address_from_public_key(public_key: PublicKey) -> bytes:
    sha = hashlib.sha256()
    rip = hashlib.new("ripemd160")
    sha.update(public_key.key)
    rip.update(sha.digest())
    return rip.digest()


def amino_pubkey_from_public_key(public_key: PublicKey) -> bytes:
    arr = bytes.fromhex(BECH32_AMINO_PUBKEY_DATA_PREFIX_SECP256K1)
    arr += bytes(public_key.key)
    return bytes(arr)


class PublicKey(JSONSerializable, ABC):
    """Data object holding the public key component of an account or signature."""

    @property
    @abstractmethod
    def type_url(self):
        pass

    @property
    @abstractmethod
    def type_amino(self):
        pass

    @abstractmethod
    def get_type(self) -> str:
        return self.type_url

    @classmethod
    def from_proto(cls, proto: Any_pb):
        type_url = proto.type_url
        value = proto.value
        if type_url == SimplePublicKey.type_url:
            return SimplePublicKey.from_proto(SimplePubKey_pb().parse(value))
        elif type_url == ValConsPubKey.type_url:
            return ValConsPubKey.from_proto(ValConsPubKey_pb().parse(value))
        elif type_url == LegacyAminoMultisigPublicKey.type_url:
            return LegacyAminoMultisigPublicKey.from_proto(
                LegacyAminoPubKey_pb().parse(value)
            )
        raise TypeError("could not marshal PublicKey: type is incorrect")

    @classmethod
    def from_amino(cls, amino: dict):
        type_amino = amino.get("type")
        if type_amino == SimplePublicKey.type_amino:
            return SimplePublicKey.from_amino(amino)
        elif type_amino == ValConsPubKey.type_amino:
            return ValConsPubKey.from_amino(amino)
        elif type_amino == LegacyAminoMultisigPublicKey.type_amino:
            return LegacyAminoMultisigPublicKey.from_amino(amino)
        raise TypeError("could not marshal PublicKey: type is incorrect")

    @classmethod
    def from_data(cls, data: dict):
        type_url = data["@type"]
        if type_url == SimplePublicKey.type_url:
            return SimplePublicKey.from_data(data)
        elif type_url == ValConsPubKey.type_url:
            return ValConsPubKey.from_data(data)
        elif type_url == LegacyAminoMultisigPublicKey.type_url:
            return LegacyAminoMultisigPublicKey.from_data(data)
        raise TypeError("could not unmarshal PublicKey: type is incorrect")

    @classmethod
    def unpack_any(cls, any_pb: Any_pb):
        unpack = create_demux_unpack_any(
            [SimplePublicKey, ValConsPubKey, LegacyAminoMultisigPublicKey]
        )
        return unpack(any_pb)

    @abstractmethod
    def pack_any(self) -> Any_pb:
        raise NotImplementedError

    @abstractmethod
    def address(self) -> str:
        pass

    @abstractmethod
    def raw_address(self) -> str:
        pass

    @abstractmethod
    def encode_amino_pubkey(self) -> bytes:
        pass

    @abstractmethod
    def to_amino(self) -> dict:
        pass

    @abstractmethod
    def to_data(self) -> dict:
        pass

    @abstractmethod
    def to_proto(self):
        pass


@attr.s
class SimplePublicKey(PublicKey):
    """Data object holding the SIMPLE public key component of an account or signature."""

    type_amino = "tendermint/PubKeySecp256k1"
    """"""
    type_url = "/cosmos.crypto.secp256k1.PubKey"
    """Normal signature public key type."""
    prototype = SimplePubKey_pb
    """"""

    key: bytes = attr.ib()

    def to_amino(self) -> dict:
        return {"type": self.type_amino, "value": base64.b64encode(self.key)}

    def to_data(self) -> dict:
        return {"@type": self.type_url, "key": base64.b64encode(self.key)}

    @classmethod
    def from_data(cls, data: dict) -> SimplePublicKey:
        return cls(key=base64.b64decode(data["key"]))

    @classmethod
    def from_proto(cls, proto: SimplePubKey_pb) -> SimplePublicKey:
        return cls(key=proto.key)

    @classmethod
    def from_amino(cls, amino: dict) -> SimplePublicKey:
        return cls(key=base64.b64decode(amino["value"]))

    def to_proto(self) -> SimplePubKey_pb:
        return SimplePubKey_pb(key=self.key)

    def get_type(self) -> str:
        return self.type_url

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))

    def encode_amino_pubkey(self) -> bytearray:
        out = bytearray.fromhex(BECH32_AMINO_PUBKEY_DATA_PREFIX_SECP256K1) + bytearray(
            self.key
        )
        return out

    def raw_address(self) -> bytes:
        return address_from_public_key(self)

    def address(self) -> str:
        return get_bech("terra", self.raw_address().hex())


@attr.s
class ValConsPubKey(PublicKey):
    """Data object holding the public key component of a validator's account or signature."""

    type_amino = "tendermint/PubKeyEd25519"
    """"""
    type_url = "/cosmos.crypto.ed25519.PubKey"
    """an ed25519 tendermint public key type."""
    prototype = ValConsPubKey_pb
    """"""

    key: bytes = attr.ib()

    def to_amino(self) -> dict:
        return {"type": self.type_amino, "value": base64.b64encode(self.key)}

    def to_data(self) -> dict:
        return {"@type": self.type_url, "key": base64.b64encode(self.key)}

    @classmethod
    def from_data(cls, data: dict) -> ValConsPubKey:
        return cls(key=base64.b64decode(data["key"]))

    @classmethod
    def from_amino(cls, amino: dict) -> ValConsPubKey:
        return cls(key=base64.b64decode(amino["value"]))

    @classmethod
    def from_proto(cls, proto: ValConsPubKey_pb) -> ValConsPubKey:
        return cls(key=proto.key)

    def get_type(self) -> str:
        return self.type_url

    def to_proto(self) -> ValConsPubKey_pb:
        return ValConsPubKey_pb(key=base64.b64encode(self.key))

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))

    def encode_amino_pubkey(self) -> bytes:
        return bytes.fromhex(BECH32_AMINO_PUBKEY_DATA_PREFIX_ED25519) + bytes(self.key)

    def raw_address(self) -> bytes:
        return address_from_public_key(self)

    def address(self) -> str:
        return get_bech("terravalcons", self.raw_address().hex())


@attr.s
class LegacyAminoMultisigPublicKey(PublicKey):
    """Data object holding the Legacy Amino-typed public key component of an account or signature."""

    type_amino = "tendermint/PubKeyMultisigThreshold"
    """"""
    type_url = "/cosmos.crypto.multisig.LegacyAminoPubKey"
    """Multisig public key type."""
    prototype = LegacyAminoPubKey_pb
    """"""

    threshold: int = attr.ib(converter=int)
    public_keys: List[SimplePublicKey] = attr.ib(factory=list)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "threshold": str(self.threshold),
                "pubkeys": [pubkey.to_amino() for pubkey in self.public_keys],
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "threshold": self.threshold,
            "public_keys": self.public_keys,
        }

    @classmethod
    def from_data(cls, data: dict) -> LegacyAminoMultisigPublicKey:
        return cls(
            threshold=data["threshold"],
            public_keys=[PublicKey.from_data(pubkey) for pubkey in data["public_keys"]],
        )

    @classmethod
    def from_proto(cls, proto: LegacyAminoPubKey_pb) -> LegacyAminoMultisigPublicKey:
        return cls(
            threshold=proto.threshold,
            public_keys=[PublicKey.unpack_any(pk) for pk in proto.public_keys],
        )

    @classmethod
    def from_amino(cls, amino: dict) -> LegacyAminoMultisigPublicKey:
        return cls(
            threshold=amino["value"]["threshold"],
            public_keys=[
                SimplePublicKey.from_amino(pubkey)
                for pubkey in amino["value"]["public_keys"]
            ],
        )

    def get_type(self) -> str:
        return self.type_url

    def to_proto(self) -> LegacyAminoPubKey_pb:
        return LegacyAminoPubKey_pb(
            threshold=self.threshold,
            public_keys=[pk.pack_any() for pk in self.public_keys],
        )

    def encode_amino_pubkey(self) -> bytearray:
        if self.threshold > 127:
            raise ValueError("threshold over 127 is now supported here")
        out = bytearray.fromhex(BECH32_AMINO_PUBKEY_DATA_PREFIX_MULTISIG_THRESHOLD)
        out.append(0x08)
        out += bytearray(encode_uvarint(self.threshold))
        for pkData in [pubkey.encode_amino_pubkey() for pubkey in self.public_keys]:
            out.append(0x12)
            out += bytearray(encode_uvarint(len(pkData)))
            out += pkData
        return out

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))

    def raw_address(self) -> str:
        pubkey_data = bytes(self.encode_amino_pubkey())
        hasher = hashlib.sha256()
        hasher.update(pubkey_data)
        return hasher.digest()[0:20].hex()

    def address(self) -> str:
        address = get_bech("terra", self.raw_address())
        return address

    def pubkey_address(self) -> str:
        return get_bech("terrapub", str(self.encode_amino_pubkey()))
