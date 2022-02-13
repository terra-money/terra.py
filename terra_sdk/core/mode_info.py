"""Data objects about Signing Mode Info."""

from __future__ import annotations

import attr

from typing import List, Optional

from terra_sdk.util.json import JSONSerializable

from terra_proto.cosmos.tx.v1beta1 import ModeInfo as ModeInfo_pb
from terra_proto.cosmos.tx.v1beta1 import ModeInfoMulti as ModeInfoMulti_pb
from terra_proto.cosmos.tx.v1beta1 import ModeInfoSingle as ModeInfoSingle_pb

from .compact_bit_array import CompactBitArray

__all__ = [
    "ModeInfo",
    "ModeInfoSingle",
    "ModeInfoMulti",
]

from terra_proto.cosmos.tx.signing.v1beta1 import SignMode


@attr.s
class ModeInfo(JSONSerializable):

    single: Optional[ModeInfoSingle] = attr.ib(default=None)
    multi: Optional[ModeInfoMulti] = attr.ib(default=None)

    def to_data(self) -> dict:
        if self.single:
            return {"single": self.single.to_data()}
        if self.multi:
            return {"multi": self.multi.to_data()}
        raise ValueError('ModeInfo should have one of single or multi')

    @classmethod
    def from_data(cls, data: dict) -> ModeInfo:
        if data.get("single"):
            return cls(single=data.get("single"))
        if data.get("multi"):
            return cls(multi=data.get("multi"))
        raise ValueError('ModeInfo should have one of single or multi')

    def to_proto(self) -> ModeInfo_pb:
        if self.single:
            return ModeInfo_pb(single=self.single.to_proto())
        else:
            return ModeInfo_pb(multi=self.multi.to_proto())

    @classmethod
    def from_proto(cls, proto: ModeInfo_pb) -> ModeInfo:
        if proto["single"]:
            return ModeInfo(single=ModeInfoSingle.from_proto(proto["single"]))
        else:
            return ModeInfo(multi=ModeInfoMulti.from_proto(proto["multi"]))


@attr.s
class ModeInfoSingle(JSONSerializable):
    mode: SignMode = attr.ib()

    def to_data(self) -> dict:
        return {"mode": self.mode}

    @classmethod
    def from_data(cls, data: dict) -> ModeInfoSingle:
        return cls(data["mode"])

    def to_proto(self) -> ModeInfoSingle_pb:
        return ModeInfoSingle_pb(mode=self.mode)

    @classmethod
    def from_proto(cls, proto: ModeInfoSingle_pb) -> ModeInfoSingle:
        mode = SignMode.from_string(proto["mode"])
        return cls(mode=mode)


@attr.s
class ModeInfoMulti(JSONSerializable):
    bitarray: CompactBitArray = attr.ib()
    mode_infos: List[ModeInfo] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> ModeInfoMulti:
        return cls(data["bitarray"], data["mode_infos"])

    def to_proto(self) -> ModeInfoMulti_pb:
        proto = ModeInfoMulti_pb()
        proto.bitarray = self.bitarray.to_proto()
        proto.mode_infos = [mi.to_proto() for mi in self.mode_infos]
        return proto

    @classmethod
    def from_proto(cls, proto: ModeInfoMulti_pb) -> ModeInfoMulti:
        return cls(
            CompactBitArray.from_proto(proto["bitarray"]),
            ModeInfo_pb.from_proto(proto["mode_infos"]),
        )
