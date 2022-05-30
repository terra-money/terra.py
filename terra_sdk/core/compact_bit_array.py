"""CompactBitArray types related to multisig."""
from __future__ import annotations

import base64
import math

import attr
from terra_proto.cosmos.crypto.multisig.v1beta1 import (
    CompactBitArray as CompactBitArray_pb,
)

from terra_sdk.util.json import JSONSerializable

__all__ = ["CompactBitArray"]


@attr.s
class CompactBitArray(JSONSerializable):
    extra_bits_stored: int = attr.ib(converter=int)
    elems: bytearray = attr.ib(converter=bytearray)

    @classmethod
    def from_data(cls, data: dict) -> CompactBitArray:
        return cls(
            data["extra_bits_stored"], bytearray(base64.b64decode(data["elems"]))
        )

    def to_data(self) -> dict:
        return {
            "extra_bits_stored": self.extra_bits_stored,
            "elems": base64.b64encode(self.elems),
        }

    @classmethod
    def from_proto(cls, proto: CompactBitArray_pb) -> CompactBitArray:
        return cls(proto.extra_bits_stored, bytearray(proto.elems))

    def to_proto(self) -> CompactBitArray_pb:
        return CompactBitArray_pb(
            extra_bits_stored=self.extra_bits_stored, elems=bytes(self.elems)
        )

    @classmethod
    def from_bits(cls, bits: int) -> CompactBitArray:
        if bits <= 0:
            raise ValueError("CompactBitArray bits must be bigger than 0")

        num_elems = (bits + 7) // 8
        if num_elems <= 0 or num_elems > (math.pow(2, 32) - 1):
            raise ValueError("CompactBitArray overflow")

        return CompactBitArray(bits % 8, bytearray(num_elems))

    def count(self) -> int:
        if self.extra_bits_stored == 0:
            return len(self.elems) * 8
        return (len(self.elems) - 1) * 8 + self.extra_bits_stored

    def get_index(self, i: int) -> bool:
        if i < 0 or i >= self.count():
            return False
        return (self.elems[(i >> 3)] & (1 << (7 - (i % 8)))) > 0

    def set_index(self, i: int, v: bool) -> bool:
        if i < 0 or i >= self.count():
            return False
        if v:  # True
            self.elems[i >> 3] |= 1 << (7 - (i % 8))
        else:  # False
            self.elems[i >> 3] &= ~(1 << (7 - (i % 8)))
        return True

    def num_true_bits_before(self, index: int) -> int:
        def count_one_bits(n: int):
            return len("".join("{0:b}".format(n).split("0")))

        ones_count = 0
        _max = self.count()
        if index > _max:
            index = _max

        elem = 0
        while True:
            if (elem * 8 + 7) >= index:
                ones_count += count_one_bits(self.elems[elem] >> (7 - (index % 8) + 1))
                return ones_count
            ones_count += count_one_bits(self.elems[elem])
            elem += 1
