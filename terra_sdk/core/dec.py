from __future__ import annotations

import re
from decimal import Decimal

from terra_sdk.util.serdes import JsonDeserializable, JsonSerializable
from terra_sdk.util.validation import Schemas as S

SDK_DEC_PREC = 18
SDK_DEC_UNIT = 10 ** SDK_DEC_PREC
SDK_DEC_REGEX_PATTERN = r"^(\-)?(\d+)(\.\d+)?\Z"
PATTERN = re.compile(SDK_DEC_REGEX_PATTERN)

__all__ = ["SDK_DEC_PREC", "Dec"]


class Dec(JsonSerializable, JsonDeserializable):

    def __init__(self, arg):
        """BigInt-based Decimal representation with basic arithmetic operations with
        compatible Python numeric types (int, float, Decimal). Does not work with
        NaN, Infinity, +0, -0, etc. Serializes as a string with 18 points of decimal
        precision.
        """
        if isinstance(arg, float):
            arg = str("%f" % arg)
        if isinstance(arg, str):
            parts = PATTERN.match(arg)
            if parts is None:
                raise ValueError(f"Unable to parse Dec object from string: {arg}")
            self.i = int(parts.group(2)) * SDK_DEC_UNIT  # integer part
            if parts.group(3):
                fraction = (
                    parts.group(3).lstrip(".")[0:SDK_DEC_PREC].ljust(SDK_DEC_PREC, "0")
                )
                self.i += int(fraction)
            if parts.group(1) is not None:
                self.i *= -1
        elif isinstance(arg, int):
            self.i = arg * SDK_DEC_UNIT
        elif isinstance(arg, Dec):
            self.i = arg.i
        elif isinstance(arg, Decimal):
            whole = int(arg)
            fraction = arg % 1
            self.i = (whole * SDK_DEC_UNIT) + (fraction * SDK_DEC_UNIT)
        else:
            raise TypeError(f"Unable to create Dec object from given argument {arg}")
        # guarantee int
        self.i = int(self.i)

    @property
    def short_str(self):
        parity = "-" if self.i < 0 else ""
        frac = self.frac.rstrip("0")
        dot = "." if len(frac) > 0 else ""
        return f"{parity}{self.whole}{dot}{frac}"

    def __repr__(self):
        return f"Dec({self.short_str!r})"  # short representation

    def __str__(self) -> str:
        if self.i == 0:
            return "0." + SDK_DEC_PREC * "0"
        parity = "-" if self.i < 0 else ""
        return f"{parity}{self.whole}.{self.frac}"

    def __int__(self) -> int:
        int_part = abs(self.i) // SDK_DEC_UNIT
        int_part *= -1 if self.i < 0 else 1
        return int_part

    def __float__(self) -> float:
        # NOTE: This is not robust enough for: float(Dec(float)) to give the same output,
        # and should mainly be used as getting a rough value from the Dec object.
        return self.i / SDK_DEC_UNIT

    @property
    def parity(self) -> int:
        return -1 if self.i < 0 else 1

    @property
    def whole(self) -> str:
        return str(abs(self.i) // SDK_DEC_UNIT)

    @property
    def frac(self) -> str:
        return str(abs(self.i) % SDK_DEC_UNIT).rjust(SDK_DEC_PREC, "0")

    def to_data(self) -> str:
        return str(self)

    def _pretty_repr_(self, path: str = ""):
        return self.short_str

    def __eq__(self, other) -> bool:
        try:
            return self._i_binop(other, int.__eq__, "==")
        except TypeError:
            return False

    def __lt__(self, other) -> bool:
        if isinstance(other, Dec):
            return self.i < other.i
        return (Decimal(self.i) / SDK_DEC_UNIT) < other

    def __le__(self, other) -> bool:
        return self < other or self == other

    def __gt__(self, other) -> bool:
        if isinstance(other, Dec):
            return self.i > other.i
        return (Decimal(self.i) / SDK_DEC_UNIT) > other

    def __ge__(self, other) -> bool:
        return self > other or self == other

    def __add__(self, other) -> Dec:
        new_val = self._i_binop(other, int.__add__, "+")
        nd = Dec(0)
        nd.i = new_val
        return nd

    def __radd__(self, other):
        return Dec.__add__(Dec(other), self)

    def __sub__(self, other) -> Dec:
        new_val = self._i_binop(other, int.__sub__, "-")
        nd = Dec(0)
        nd.i = new_val
        return nd

    def __rsub__(self, other):
        return Dec.__sub__(Dec(other), self)

    def __mul__(self, other):
        if isinstance(other, Dec):
            new_val = self.i * other.i
        elif (
            isinstance(other, int)
            or isinstance(other, float)
            or isinstance(other, Decimal)
        ):
            new_val = self.i * Dec(other).i
        else:
            raise TypeError(
                f"unsupported operand types for *: 'Dec' and '{type(other)}'"
            )
        nd = Dec(0)
        nd.i = new_val // SDK_DEC_UNIT
        return nd

    def __rmul__(self, other):
        return Dec.__mul__(Dec(other), self)

    def __truediv__(self, other):
        try:
            # we need the decimal value's better precision.
            d1 = Decimal(self.i)
            d2 = Decimal(other.i)
            new_val = d1 / d2
        except AttributeError:
            new_val = self._i_binop(other, int.__truediv__, "/")
        nd = Dec(0)
        nd.i = int(new_val * SDK_DEC_UNIT)
        return nd

    def __rtruediv__(self, other):
        return Dec.__truediv__(Dec(other), self)

    def __floordiv__(self, other):
        return Dec(int(self / Dec(other)))

    def __neg__(self):
        x = Dec(self)
        x.i *= -1
        return x

    def __abs__(self):
        x = Dec(self)
        x.i = abs(x.i)
        return x

    def __pos__(self):
        return abs(self)

    @classmethod
    def from_data(cls, data: str) -> Dec:
        return cls(data)

    @classmethod
    def with_prec(cls, i: int, prec: int) -> Dec:
        """Replicates Dec.with_prec(i, prec)"""
        d = cls(0)
        i = int(i)
        d.i = i * 10 ** (SDK_DEC_PREC - int(prec))
        return d

    def _i_binop(self, other, binop, binop_name):
        """Helper method that tries to work with compatible number types by first converting
        them into Dec and working with their internal BigInt representation.
        """
        if isinstance(other, Dec):
            new_val = binop(self.i, other.i)
        elif (
            isinstance(other, int)
            or isinstance(other, float)
            or isinstance(other, Decimal)
        ):
            new_val = binop(self.i, Dec(other).i)
        else:
            raise TypeError(
                f"unsupported operand types for {binop_name}: 'Dec' and '{type(other)}'"
            )
        return new_val
