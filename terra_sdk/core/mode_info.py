"""Data objects about Signing Mode Info."""

from __future__ import annotations

from typing import List, Optional

import attr
from terra_proto.cosmos.tx.v1beta1 import ModeInfo as ModeInfo_pb
from terra_proto.cosmos.tx.v1beta1 import ModeInfoMulti as ModeInfoMulti_pb
from terra_proto.cosmos.tx.v1beta1 import ModeInfoSingle as ModeInfoSingle_pb

from terra_sdk.util.json import JSONSerializable

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
        raise ValueError("ModeInfo should have one of single or multi")

    @classmethod
    def from_data(cls, data: dict) -> ModeInfo:
        if data.get("single"):
            return cls(single=ModeInfoSingle.from_data(data.get("single")))
        if data.get("multi"):
            return cls(multi=ModeInfoMulti.from_data(data.get("multi")))
        raise ValueError("ModeInfo should have one of single or multi")

    def to_proto(self) -> ModeInfo_pb:
        if self.single:
            return ModeInfo_pb(single=self.single.to_proto())
        else:
            return ModeInfo_pb(multi=(self.multi.to_proto() if self.multi else None))

    @classmethod
    def from_proto(cls, proto: ModeInfo_pb) -> ModeInfo:
        if proto.single is not None:
            return ModeInfo(single=ModeInfoSingle.from_proto(proto.single))
        else:
            return ModeInfo(multi=ModeInfoMulti.from_proto(proto.multi))


@attr.s
class ModeInfoSingle(JSONSerializable):
    mode: SignMode = attr.ib()

    def to_data(self) -> dict:
        return {"mode": self.mode.name}

    @classmethod
    def from_data(cls, data: dict) -> ModeInfoSingle:
        return cls(SignMode[data["mode"]])

    def to_proto(self) -> ModeInfoSingle_pb:
        return ModeInfoSingle_pb(mode=self.mode)

    @classmethod
    def from_proto(cls, proto: ModeInfoSingle_pb) -> ModeInfoSingle:
        mode = SignMode(proto.mode)
        return cls(mode=mode)


@attr.s
class ModeInfoMulti(JSONSerializable):
    bitarray: CompactBitArray = attr.ib()
    mode_infos: List[ModeInfo] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> ModeInfoMulti:
        return cls(
            CompactBitArray.from_data(data["bitarray"]),
            [ModeInfo.from_data(d) for d in data["mode_infos"]],
        )

    def to_data(self) -> dict:
        return {
            "bitarray": self.bitarray.to_data(),
            "mode_infos": [mi.to_data() for mi in self.mode_infos],
        }

    def to_proto(self) -> ModeInfoMulti_pb:
        return ModeInfoMulti_pb(
            bitarray=self.bitarray.to_proto(),
            mode_infos=[mi.to_proto() for mi in self.mode_infos],
        )

    @classmethod
    def from_proto(cls, proto: ModeInfoMulti_pb) -> ModeInfoMulti:
        return cls(
            CompactBitArray.from_proto(proto.bitarray),
            ModeInfo_pb.from_proto(proto.mode_infos),
        )
