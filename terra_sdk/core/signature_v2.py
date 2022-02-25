"""Data objects about Signature V2."""

from __future__ import annotations

import base64
from typing import Dict, List, Optional

import attr
from terra_proto.cosmos.tx.v1beta1 import (
    ModeInfoSingle as ModeInfoSingle_pb,
    ModeInfoMulti as ModeInfoMulti_pb,
)
from terra_proto.cosmos.tx.signing.v1beta1 import SignMode

from .public_key import PublicKey
from .mode_info import ModeInfo, ModeInfoSingle, ModeInfoMulti
from .compact_bit_array import CompactBitArray

from terra_proto.cosmos.crypto.multisig.v1beta1 import (
    MultiSignature as MultiSignature_pb,
)

__all__ = ["SignatureV2", "Descriptor", "Single", "Multi", "SignMode"]

from terra_sdk.util.json import JSONSerializable


@attr.s
class SignatureV2:
    public_key: PublicKey = attr.ib()
    data: Descriptor = attr.ib()
    sequence: int = attr.ib(converter=int)

    @classmethod
    def from_data(cls, data: dict) -> SignatureV2:
        return cls(
            public_key=PublicKey.from_data(data["public_key"]),
            data=Descriptor.from_data(data["data"]),
            sequence=data["sequence"],
        )

    def to_data(self) -> dict:
        return {
            "public_key": self.public_key.to_data(),
            "data": self.data.to_data(),
            "sequence": self.sequence
        }


@attr.s
class Descriptor:
    single: Optional[Single] = attr.ib(default=None)
    multi: Optional[Multi] = attr.ib(default=None)

    @classmethod
    def from_data(cls, data: dict) -> Descriptor:
        s = None
        m = None
        if data["single"] is not None:
            s = Single.from_data(data["single"])
        if data["multi"] is not None:
            m = Multi.from_data(data["multi"])
        return cls(single=s, multi=m)

    def to_data(self) -> dict:
        typ = "single" if self.single else "multi"
        dat = self.single.to_data() if self.single else self.multi.to_data()
        return {
            typ: dat
        }

    def to_mode_info_and_signature(self) -> [ModeInfo, bytes]:
        if self.single is not None:
            sig_data = self.single
            return [
                ModeInfo(single=ModeInfoSingle(sig_data.mode)),
                sig_data.signature
            ]

        if self.multi:
            sig_data = self.multi
            mode_infos: List[ModeInfo] = []
            signatures: List[bytes] = []
            for sig in sig_data.signatures:
                mode_info, sig_bytes = sig.to_mode_info_and_signature()
                mode_infos.append(mode_info)
                signatures.append(sig_bytes)
            pb = MultiSignature_pb(signatures=signatures)
            return [
                ModeInfo(multi=ModeInfoMulti(sig_data.bitarray, mode_infos)),
                base64.b64encode(bytes(pb))
            ]

        raise ValueError('invalid signature descriptor')


@attr.s
class Single:  # FIXME: SignModeTo/FromJSON
    mode: SignMode = attr.ib()
    signature: bytes = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> Single:
        return cls(mode=data["mode"], signature=data["signature"])

    def to_data(self) -> dict:
        return {
            "mode": self.mode,
            "signature": self.signature
        }


@attr.s
class Multi:
    bitarray: CompactBitArray = attr.ib()
    signatures: List[Descriptor] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> Multi:
        return cls(
            CompactBitArray.from_data(data["bitarray"]),
            [Descriptor.from_data(d) for d in data["signatures"]],
        )

    def to_data(self) -> dict:
        return {
            "bitarray": self.bitarray.to_data(),
            "signatures": [sig.to_data() for sig in self.signatures]
        }
