"""Data objects about Signature V2."""

from __future__ import annotations

from typing import Dict, List, Optional

import attr

from terra_sdk.core.tx import CompactBitArray
from terra_sdk.core.public_key import PublicKey

__all__ = ["SignatureV2", "Descriptor", "Single", "Multi"]


@attr.s
class SignatureV2:
    public_key: PublicKey = attr.ib()
    data: Descriptor = attr.ib()
    sequence: int = attr.ib(converter=int)

    @classmethod
    def from_data(cls, data: dict) -> SignatureV2:
        data = data["value"]
        return cls(
            public_key=PublicKey.from_data(data["public_key"]),
            data=Descriptor.from_data(data["data"]),
            sequence=data["sequence"]
        )


@attr.s
class Descriptor:
    single: Optional[Single] = attr.ib(default=None)
    multi: Optional[Multi] = attr.ib(default=None)

    @classmethod
    def from_data(cls, data: dict) -> Descriptor:
        data = data["value"]
        if data["single"] is not None:
            s = Single.from_data(data["single"])
        if data["multi"] is not None:
            m = Multi.from_data(data["multi"])
        return cls(single=s, multi=m)


@attr.s
class Single:
    mode: str = attr.ib()
    signature: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> Single:
        data = data["value"]
        return cls(mode=data["mode"], signature=data["signature"])


@attr.s
class Multi:
    bitarray: CompactBitArray = attr.ib()
    signatures: List[Descriptor] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> Multi:
        data = data["value"]
        return cls(
            CompactBitArray.from_data(data["bitarray"]),
            [Descriptor.from_data(d) for d in data["signatures"]]
        )
