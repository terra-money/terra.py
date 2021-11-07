"""Data objects about Signature V2."""

from __future__ import annotations

from typing import Dict, List, Optional

import attr
from terra_proto.cosmos.tx.signing.v1beta1 import (
    SignatureDescriptor as SignatureDescriptor_pb,
)
from terra_proto.cosmos.tx.signing.v1beta1 import (
    SignatureDescriptorDataMulti as SignatureDescriptorDataMulti_pb,
)
from terra_proto.cosmos.tx.signing.v1beta1 import (
    SignatureDescriptorDataSingle as SignatureDescriptorDataSingle_pb,
)
from terra_proto.cosmos.tx.signing.v1beta1 import SignMode

from terra_sdk.core.public_key import PublicKey
from terra_sdk.core.tx import CompactBitArray

__all__ = ["SignatureV2", "Descriptor", "Single", "Multi", "SignMode"]


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


@attr.s
class Descriptor:
    single: Optional[Single] = attr.ib(default=None)
    multi: Optional[Multi] = attr.ib(default=None)

    @classmethod
    def from_data(cls, data: dict) -> Descriptor:
        if data["single"] is not None:
            s = Single.from_data(data["single"])
        if data["multi"] is not None:
            m = Multi.from_data(data["multi"])
        return cls(single=s, multi=m)


@attr.s
class Single:
    mode: SignMode = attr.ib()
    signature: bytes = attr.ib()

    def to_proto(self) -> SignatureDescriptorDataSingle_pb:
        return SignatureDescriptorDataSingle_pb(
            mode=self.mode, signature=self.signature
        )

    @classmethod
    def from_data(cls, data: dict) -> Single:
        return cls(mode=data["mode"], signature=data["signature"])


@attr.s
class Multi:
    bitarray: CompactBitArray = attr.ib()
    signatures: List[Descriptor] = attr.ib()

    def to_proto(self) -> SignatureDescriptorDataMulti_pb:
        return SignatureDescriptorDataMulti_pb(
            bitarray=self.bitarray.to_proto(),
            signatures=[sig.to_proto() for sig in self.signatures],
        )

    @classmethod
    def from_data(cls, data: dict) -> Multi:
        return cls(
            CompactBitArray.from_data(data["bitarray"]),
            [Descriptor.from_data(d) for d in data["signatures"]],
        )
