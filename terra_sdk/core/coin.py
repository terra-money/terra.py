from __future__ import annotations

import math
import re
from typing import Union

import attr
from terra_proto.cosmos.base.v1beta1 import Coin as Coin_pb

from terra_sdk.util.json import JSONSerializable

from .numeric import Dec, Numeric


@attr.s(frozen=True)
class Coin(JSONSerializable):
    """Represents a (denom, amount) pairing, analagous to ``sdk.Coin`` and ``sdk.DecCoin``
    in Cosmos SDK. Used for representing Terra native assets.
    """

    denom: str = attr.ib()
    """Coin's denomination, only ``uluna``."""

    amount: Numeric.Output = attr.ib(converter=Numeric.parse)  # type: ignore
    """Coin's amount -- can be a ``int`` or :class:`Dec`"""

    @staticmethod
    def parse(arg: Union[Coin, str, dict]) -> Coin:
        """Converts the argument into a coin.

        Args:
            arg (Union[Coin, str, dict]): value to be converted to coin
        """
        if isinstance(arg, Coin):
            return arg
        elif isinstance(arg, str):
            return Coin.from_str(arg)
        else:
            return Coin.from_data(arg)

    def is_int_coin(self) -> bool:
        """Checks whether the coin's amount is of type ``int``."""
        return isinstance(self.amount, int)

    def is_dec_coin(self) -> bool:
        """Checks whether the coin's amount is of type :class:`Dec`."""
        return isinstance(self.amount, Dec)

    def to_int_coin(self) -> Coin:
        """Creates a new :class:`Coin` with an ``int`` amount."""
        return Coin(self.denom, int(self.amount))

    def to_int_ceil_coin(self) -> Coin:
        """Turns the :class:`coin` into an ``int`` coin with ceiling the amount."""
        return Coin(self.denom, int(math.ceil(self.amount)))

    def to_dec_coin(self) -> Coin:
        """Creates a new :class:`Coin` with a :class:`Dec` amount."""
        return Coin(self.denom, Dec(self.amount))

    def __str__(self) -> str:
        if self.is_dec_coin():
            amount_str = str(self.amount).rstrip("0")
            if amount_str.endswith("."):
                amount_str += "0"
            return f"{amount_str}{self.denom}"
        return f"{self.amount}{self.denom}"

    def to_amino(self) -> dict:
        return {"denom": self.denom, "amount": str(self.amount)}

    def to_data(self) -> dict:
        return {"denom": self.denom, "amount": str(self.amount)}

    @classmethod
    def from_proto(cls, proto: Coin_pb) -> Coin:
        return cls(proto.denom, proto.amount)

    def to_proto(self) -> Coin_pb:
        coin = Coin_pb()
        coin.denom = self.denom
        coin.amount = str(self.amount)
        return coin

    @classmethod
    def from_str(cls, string: str) -> Coin:
        """Creates a new :class:`Coin` from a coin-format string. Must match the format:
        ``283923uluna`` (``int``-Coin) or ``23920.23020uluna`` (:class:`Dec`-Coin).

        >>> int_coin = Coin.from_str("230920uluna")
        >>> int_coin.denom
        'uluna'
        >>> int_coin.amount
        230920
        >>> dec_coin = Coin.from_str("203922.223uluna")
        >>> dec_coin.denom
        'uluna'
        >>> dec_coin.amount
        Dec('203922.223')

        Args:
            string (str): string to convert

        Raises:
            ValueError: if string is in wrong format

        Returns:
            Coin: converted string
        """
        pattern = r"^(\-?[0-9]+(\.[0-9]+)?)([0-9a-zA-Z/]+)$"
        match = re.match(pattern, string)
        if match is None:
            raise ValueError(f"failed to parse Coin: {string}")
        else:
            return cls(match.group(3), match.group(1))

    def add(self, addend: Union[Numeric.Input, Coin]) -> Coin:
        """Creates a new :class:`Coin` with the sum as amount. If the ``addend`` is a
        :class:`Coin`, its ``denom`` must match.

        Args:
            addend (Union[Numeric.Input, Coin]): addend

        Raises:
            ArithmeticError: if addedend has different ``denom``

        Returns:
            Coin: sum
        """
        if isinstance(addend, Coin):
            if addend.denom != self.denom:
                raise ArithmeticError(
                    f"cannot add/subtract two Coin objects of different denoms: {self.denom} and {addend.denom}"
                )
            return Coin(self.denom, self.amount + addend.amount)
        else:
            return Coin(self.denom, self.amount + Numeric.parse(addend))

    def __add__(self, addend: Union[Numeric.Input, Coin]) -> Coin:
        return self.add(addend)

    def sub(self, subtrahend: Union[Numeric.Input, Coin]) -> Coin:
        """Creates a new :class:`Coin` with the difference as amount. If the ``subtrahend`` is a
        :class:`Coin`, its ``denom`` must match.

        Args:
            subtrahend (Union[Numeric.Input, Coin]): subtrahend

        Returns:
            Coin: difference
        """
        if isinstance(subtrahend, Coin):
            return self.add(subtrahend.mul(-1))
        else:
            return self.add(Numeric.parse(subtrahend) * -1)

    def __sub__(self, subtrahend: Union[Numeric.Input, Coin]) -> Coin:
        return self.sub(subtrahend)

    def mul(self, multiplier: Numeric.Input) -> Coin:
        """Creates a new :class:`Coin` with the product as amount. The ``multiplier``
        argument is first coerced to either an ``int`` or :class:`Dec`.

        Args:
            multiplier (Numeric.Input): multiplier

        Returns:
            Coin: product
        """
        other_amount = Numeric.parse(multiplier)
        return Coin(self.denom, self.amount * other_amount)

    def __mul__(self, multiplier: Numeric.Input) -> Coin:
        return self.mul(multiplier)

    def div(self, divisor: Numeric.Input) -> Coin:
        """Creates a new :class:`Coin` with the quotient as amount. The ``divisor``
        argument is first coerced to either an ``int`` or :class:`Dec`.

        Args:
            divisor (Numeric.Input): divisor

        Returns:
            Coin: quotient
        """
        other_amount = Numeric.parse(divisor)
        if isinstance(other_amount, int):
            return Coin(self.denom, (self.amount // other_amount))
        else:
            return Coin(self.denom, (self.amount / other_amount))

    def __truediv__(self, divisor: Numeric.Input) -> Coin:
        return self.div(divisor)

    def __floordiv__(self, divisor: Numeric.Input) -> Coin:
        return self.div(int(Numeric.parse(divisor)))

    def mod(self, modulo: Numeric.Input) -> Coin:
        """Creates a new :class:`Coin` with the modulus as amount.

        Args:
            modulo (Numeric.Input): modulo

        Returns:
            Coin: modulo
        """
        other_amount = Numeric.parse(modulo)
        if isinstance(other_amount, Dec):
            return Coin(self.denom, Dec(self.amount).mod(other_amount))
        else:
            return Coin(self.denom, self.amount % other_amount)

    def __mod__(self, modulo: Numeric.Input) -> Coin:
        return self.mod(modulo)

    def __neg__(self) -> Coin:
        return Coin(denom=self.denom, amount=(-self.amount))

    def __abs__(self) -> Coin:
        return Coin(denom=self.denom, amount=abs(self.amount))

    def __pos__(self) -> Coin:
        return abs(self)

    @classmethod
    def from_data(cls, data: dict) -> Coin:
        """Deserializes a :class:`Coin` object from its JSON data representation.

        Args:
            data (dict): data object
        """
        return cls(data["denom"], data["amount"])

    @classmethod
    def from_amino(cls, data: dict) -> Coin:
        """Deserializes a :class:`Coin` object from its amino-codec representation.

        Args:
            data (dict): data object
        """
        return cls(data["denom"], data["amount"])
