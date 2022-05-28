"""Numeric types."""

from __future__ import annotations

import re
from decimal import Decimal
from typing import Union

from terra_sdk.util.json import JSONSerializable

DEC_NUM_DIGITS = 18
"""Number of digits for Decimal."""

DEC_ONE = 10**DEC_NUM_DIGITS
DEC_PATTERN = re.compile(r"^(\-)?(\d+)(\.(\d+))?\Z")

__all__ = ["DEC_NUM_DIGITS", "Dec", "Numeric"]


def convert_to_dec_bignum(arg: Union[str, int, float, Decimal]):
    if isinstance(arg, int) or isinstance(arg, Decimal):
        return int(arg * DEC_ONE)
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


class Dec(JSONSerializable):
    """BigInt-based Decimal representation with basic arithmetic operations with
    compatible Python numeric types (int, float, Decimal). Does not work with
    ``NaN``, ``Infinity``, ``+0``, ``-0``, etc. Serializes as a string with 18 points of
    decimal precision.

    >>> Dec(5)
    Dec("5.0")
    >>> Dec("121.1232")
    Dec("121.1232")
    >>> Dec(121.1232)
    Dec("121.1232")

    Args:
        arg (Union[str, int, float, Decimal, Dec]): argument to coerce into Dec
    """

    _i: int = 0

    def __init__(self, arg: Union[str, int, float, Decimal, Dec]):
        if isinstance(arg, Dec):
            self._i = arg._i
            return
        else:
            self._i = int(convert_to_dec_bignum(arg))

    @classmethod
    def zero(cls) -> Dec:
        """Dec representation of zero.

        Returns:
            Dec: zero
        """
        return cls(0)

    @classmethod
    def one(cls):
        """Dec representation of one.

        Returns:
            Dec: one
        """
        nd = cls(0)
        nd._i = DEC_ONE
        return nd

    def __str__(self) -> str:
        """Converts to a string using all 18 decimal precision points.

        Returns:
            str: string representation
        """
        if self._i == 0:
            return "0." + DEC_NUM_DIGITS * "0"
        parity = "-" if self._i < 0 else ""
        return f"{parity}{self.whole}.{self.frac}"

    def to_short_str(self) -> str:
        """Converts to a string, but truncates all unnecessary zeros.

        Returns:
            str: string representation
        """
        parity = "-" if self._i < 0 else ""
        frac = self.frac.rstrip("0")
        dot = "." if len(frac) > 0 else ""
        return f"{parity}{self.whole}{dot}{frac}"

    def __repr__(self):
        return f"Dec('{self.to_short_str()}')"  # short representation

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
        """Get the parity of the Dec value. Returns -1 if value is below 0, and 1 otherwise.

        Returns:
            int: parity
        """
        return -1 if self._i < 0 else 1

    @property
    def whole(self) -> str:
        """Get the integral part of the Dec value.

        Returns:
            str: integer, as string
        """
        return str(abs(self._i) // DEC_ONE)

    @property
    def frac(self) -> str:
        """Get the fractional part of the Dec value.

        Returns:
            str: fraction, as string
        """
        return str(abs(self._i) % DEC_ONE).rjust(DEC_NUM_DIGITS, "0")

    def to_data(self) -> str:
        return str(self)

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return False
        else:
            return self._i == Dec(other)._i

    def lt(self, other: Union[str, int, float, Decimal, Dec]) -> bool:
        """Check less than.

        Args:
            other (Union[str, int, float, Decimal, Dec]): compared object
        """
        if isinstance(other, Dec):
            return self._i < other._i
        return (Decimal(self._i) / DEC_ONE) < other

    def __lt__(self, other: Union[str, int, float, Decimal, Dec]) -> bool:
        return self.lt(other)

    def le(self, other: Union[str, int, float, Decimal, Dec]) -> bool:
        """Check less than or equal to.

        Args:
            other (Union[str, int, float, Decimal, Dec]): compared object
        """
        return self < other or self.__eq__(other)

    def __le__(self, other: Union[str, int, float, Decimal, Dec]) -> bool:
        return self.le(other)

    def gt(self, other: Union[str, int, float, Decimal, Dec]) -> bool:
        """Check greater than.

        Args:
            other (Union[str, int, float, Decimal, Dec]): compared object
        """
        if isinstance(other, Dec):
            return self._i > other._i
        return (Decimal(self._i) / DEC_ONE) > other

    def __gt__(self, other) -> bool:
        return self.gt(other)

    def ge(self, other) -> bool:
        """Check greater than or equal to.

        Args:
            other (Union[str, int, float, Decimal, Dec]): compared object
        """
        return self.gt(other) or self.__eq__(other)

    def __ge__(self, other) -> bool:
        return self.ge(other)

    def add(self, addend: Union[str, int, float, Decimal, Dec]) -> Dec:
        """Performs addition. ``addend`` is first converted into Dec.

        Args:
            addend (Union[str, int, float, Decimal, Dec]): addend

        Returns:
            Dec: sum
        """
        nd = Dec.zero()
        nd._i = self._i + Dec(addend)._i
        return nd

    def __add__(self, addend: Union[str, int, float, Decimal, Dec]) -> Dec:
        return self.add(addend)

    def __radd__(self, addend: Union[str, int, float, Decimal, Dec]):
        return Dec(addend).add(self)

    def sub(self, subtrahend: Union[str, int, float, Decimal, Dec]) -> Dec:
        """Performs subtraction. ``subtrahend`` is first converted into Dec.

        Args:
            subtrahend (Union[str, int, float, Decimal, Dec]): subtrahend

        Returns:
            Dec: difference
        """
        nd = Dec.zero()
        nd._i = self._i - Dec(subtrahend)._i
        return nd

    def __sub__(self, subtrahend: Union[str, int, float, Decimal, Dec]) -> Dec:
        return self.sub(subtrahend)

    def __rsub__(self, minuend: Dec) -> Dec:
        return Dec(minuend).sub(self)

    def mul(self, multiplier: Union[str, int, float, Decimal, Dec]) -> Dec:
        """Performs multiplication. ``multiplier`` is first converted into Dec.

        Args:
            multiplier (Union[str, int, float, Decimal, Dec]): multiplier

        Returns:
            Dec: product
        """
        x = self._i
        y = Dec(multiplier)._i
        nd = Dec.zero()
        nd._i = chop_precision_and_round(x * y)
        return nd

    def __mul__(self, multiplier: Union[str, int, float, Decimal, Dec]) -> Dec:
        return self.mul(multiplier)

    def __rmul__(self, multiplicand: Union[str, int, float, Decimal, Dec]):
        return Dec(multiplicand).mul(self)

    def div(self, divisor: Union[str, int, float, Decimal, Dec]) -> Dec:
        """Performs division. ``divisor`` is first converted into Dec.
        It works like truediv('/')

        Args:
            divisor (Union[str, int, float, Decimal, Dec]): divisor

        Raises:
            ZeroDivisionError: if ``divisor`` is 0

        Returns:
            Dec: quotient
        """
        if Dec(divisor)._i == 0:
            raise ZeroDivisionError(f"tried to divide by 0: {self!r} / {divisor!r}")
        nd = Dec.zero()
        nd._i = chop_precision_and_round(self._i * DEC_ONE * DEC_ONE // Dec(divisor)._i)
        return nd

    def __truediv__(self, divisor) -> Dec:
        return self.div(divisor)

    def __rtruediv__(self, divisor) -> Dec:
        return Dec(divisor).div(self)

    def __floordiv__(self, divisor):
        return Dec(chop_precision_and_round(self.div(divisor).sub(0.5)._i))

    def __rfloordiv__(self, divisor):
        return Dec(chop_precision_and_round(divisor / self.sub(0.5)._i))

    def mod(self, modulo: Union[str, int, float, Decimal, Dec]) -> Dec:
        """Performs modulus. ``modulo`` is first converted into Dec.

        Args:
            modulo (Union[str, int, float, Decimal, Dec]): modulo

        Returns:
            Dec: modulus
        """
        return self.sub(self.__floordiv__(modulo).mul(modulo))

    def __mod__(self, modulo) -> Dec:
        return self.mod(modulo)

    def __neg__(self) -> Dec:
        x = Dec(self)
        x._i *= -1
        return x

    def __abs__(self) -> Dec:
        x = Dec(self)
        x._i = abs(x._i)
        return x

    def __pos__(self) -> Dec:
        # __pos__ implies a copy
        return Dec(self)

    @classmethod
    def from_data(cls, data: str) -> Dec:
        """Converts Dec-formatted string into proper :class:`Dec` object."""
        return cls(data)

    @classmethod
    def with_prec(cls, i: Union[int, str], prec: int) -> Dec:
        """Replicates Cosmos SDK's ``Dec.withPreic(i, prec)``.

        Args:
            i (Union[int, str]): numeric value
            prec (int): precision

        Returns:
            Dec: decimal
        """
        d = cls(0)
        i = int(i)
        d._i = i * 10 ** (DEC_NUM_DIGITS - int(prec))
        return d


class Numeric:

    Input = Union[str, int, float, Decimal, Dec]
    """"""

    Output = Union[int, Dec]
    """"""

    @staticmethod
    def parse(value: Numeric.Input) -> Numeric.Output:
        """Parses the value and coerces it into an ``int`` or :class:`Dec`.

        Args:
            value (Numeric.Input): value to be parsed

        Raises:
            TypeError: if supplied value could not be parsed

        Returns:
            Numeric.Output: coerced number
        """
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
