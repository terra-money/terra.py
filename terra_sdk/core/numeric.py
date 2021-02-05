from __future__ import annotations

import re
from decimal import Decimal
from typing import Union

DEC_NUM_DIGITS = 18
DEC_ONE = 10 ** DEC_NUM_DIGITS
DEC_PATTERN = re.compile(r"^(\-)?(\d+)(\.(\d+))?\Z")

__all__ = ["DEC_NUM_DIGITS", "Dec"]


def convert_to_dec_bignum(arg: Union[str, int, float, Decimal]):
    if isinstance(arg, int):
        return arg * DEC_ONE
    if isinstance(arg, float):
        arg = str("%f" % arg)
    if isinstance(arg, str):
        parts = DEC_PATTERN.match(arg)
        if parts is None:
            raise ValueError(f"Unable to parse Dec from string: {arg}")
        result = int(parts.group(2)) * DEC_ONE  # whole part
        if parts.group(3):
            fraction = int(parts.group(4)[0:DEC_NUM_DIGITS].ljust(DEC_NUM_DIGITS, "0"))
            result += fraction
        if parts.group(1):
            result *= -1
        return result
    elif isinstance(arg, Decimal):
        whole = int(arg)
        fraction = int(arg % 1)
        return int((whole * DEC_ONE) + (fraction * DEC_ONE))
    else:
        raise TypeError(
            f"Unable to parse Dec integer representation from given argument {arg}"
        )


def chop_precision_and_round(d: int) -> int:
    """Cosmos-SDK's banker's rounding:
    https://github.com/cosmos/cosmos-sdk/blob/1d75e0e984e7132efd54c3526e36b3585e2d91c0/types/decimal.go#L491
    """
    if d < 0:
        return -1 * chop_precision_and_round(d * -1)

    quo, rem = d // DEC_ONE, d % DEC_ONE

    if rem == 0:
        return quo

    if rem < DEC_ONE / 2:
        return quo
    elif rem > DEC_ONE / 2:
        return quo + 1
    else:
        if quo % 2 == 0:
            return quo
        return quo + 1


class Dec:

    _i: int = 0

    def __init__(self, arg: Union[str, int, float, Decimal, Dec]):
        """BigInt-based Decimal representation with basic arithmetic operations with
        compatible Python numeric types (int, float, Decimal). Does not work with
        NaN, Infinity, +0, -0, etc. Serializes as a string with 18 points of decimal
        DEC_NUM_DIGITS.
        """
        if isinstance(arg, Dec):
            self._i = arg._i
            return
        else:
            self._i = int(convert_to_dec_bignum(arg))

    @classmethod
    def zero(cls):
        return cls(0)

    @classmethod
    def one(cls):
        nd = cls(0)
        nd._i = DEC_ONE
        return nd

    def __str__(self) -> str:
        if self._i == 0:
            return "0." + DEC_NUM_DIGITS * "0"
        parity = "-" if self._i < 0 else ""
        return f"{parity}{self.whole}.{self.frac}"

    def to_short_str(self):
        parity = "-" if self._i < 0 else ""
        frac = self.frac.rstrip("0")
        dot = "." if len(frac) > 0 else ""
        return f"{parity}{self.whole}{dot}{frac}"

    def __repr__(self):
        return f"Dec({self.to_short_str()})"  # short representation

    def __int__(self) -> int:
        int_part = abs(self._i) // DEC_ONE
        int_part *= -1 if self._i < 0 else 1
        return int_part

    def __float__(self) -> float:
        # NOTE: This is not robust enough for: float(Dec(float)) to give the same output
        # and should mainly be used as getting a rough value from the Dec object.
        return float(self._i) / DEC_ONE

    @property
    def parity(self) -> int:
        return -1 if self._i < 0 else 1

    @property
    def whole(self) -> str:
        return str(abs(self._i) // DEC_ONE)

    @property
    def frac(self) -> str:
        return str(abs(self._i) % DEC_ONE).rjust(DEC_NUM_DIGITS, "0")

    def to_data(self) -> str:
        return str(self)

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return False
        else:
            return self._i == Dec(other)._i

    def lt(self, other) -> bool:
        if isinstance(other, Dec):
            return self._i < other._i
        return (Decimal(self._i) / DEC_ONE) < other

    def __lt__(self, other) -> bool:
        return self.lt(other)

    def le(self, other) -> bool:
        return self < other or self.__eq__(other)

    def __le__(self, other) -> bool:
        return self.le(other)

    def gt(self, other) -> bool:
        if isinstance(other, Dec):
            return self._i > other._i
        return (Decimal(self._i) / DEC_ONE) > other

    def __gt__(self, other) -> bool:
        return self.gt(other)

    def ge(self, other) -> bool:
        return self.gt(other) or self.__eq__(other)

    def __ge__(self, other) -> bool:
        return self.ge(other)

    def add(self, other) -> Dec:
        nd = Dec.zero()
        nd._i = self._i + Dec(other)._i
        return nd

    def __add__(self, other) -> Dec:
        return self.add(other)

    def __radd__(self, other):
        return Dec(other).add(self)

    def sub(self, other) -> Dec:
        nd = Dec.zero()
        nd._i = self._i - Dec(other)._i
        return nd

    def __sub__(self, other) -> Dec:
        return self.sub(other)

    def __rsub__(self, other):
        return Dec(other).sub(self)

    def mul(self, other: Union[str, int, float, Decimal, Dec]) -> Dec:
        x = self._i
        y = Dec(other)._i
        nd = Dec.zero()
        nd._i = chop_precision_and_round(x * y)
        return nd

    def __mul__(self, other) -> Dec:
        return self.mul(other)

    def __rmul__(self, other):
        return Dec(other).mul(self)

    def div(self, other) -> Dec:
        if Dec(other)._i == 0:
            raise ZeroDivisionError(f"tried to divide by 0: {self!r} / {other!r}")
        nd = Dec.zero()
        nd._i = chop_precision_and_round(self._i * DEC_ONE * DEC_ONE // Dec(other)._i)
        return nd

    def __truediv__(self, other) -> Dec:
        return self.div(other)

    def __rtruediv__(self, other) -> Dec:
        return Dec(other).div(self)

    def __floordiv__(self, other):
        return self.div(int(other))

    def mod(self, other) -> Dec:
        return self.sub(self.div(other).mul(self))

    def __mod__(self, other) -> Dec:
        return self.mod(other)

    def __neg__(self) -> Dec:
        x = Dec(self)
        x._i *= -1
        return x

    def __abs__(self) -> Dec:
        x = Dec(self)
        x._i = abs(x._i)
        return x

    def __pos__(self) -> Dec:
        return abs(self)

    @classmethod
    def from_data(cls, data: str) -> Dec:
        return cls(data)

    @classmethod
    def with_prec(cls, i: Union[int, str], prec: int) -> Dec:
        """Replicates Cosmos-SDK's Dec.with_prec(i, prec)"""
        d = cls(0)
        i = int(i)
        d._i = i * 10 ** (DEC_NUM_DIGITS - int(prec))
        return d


class Numeric:

    Input = Union[str, int, float, Decimal, Dec]
    Output = Union[int, Dec]

    @staticmethod
    def parse(value: Numeric.Input) -> Numeric.Output:
        if isinstance(value, int) or isinstance(value, Dec):
            return value
        elif isinstance(value, str):
            if "." in value:
                return Dec(value)
            else:
                return int(value)
        elif isinstance(value, float) or isinstance(value, Decimal):
            return Dec(value)
        else:
            raise TypeError(f"could not parse numeric value to Dec or int: {value}")
