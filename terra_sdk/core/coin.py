from __future__ import annotations

from typing import Union

import attr
import re

from .numeric import Dec, Numeric
from terra_sdk.util.json import JSONSerializable


@attr.s(frozen=True)
class Coin(JSONSerializable):

    denom: str = attr.ib()
    amount: Numeric.Output = attr.ib(converter=Numeric.parse)

    @staticmethod
    def parse(arg: Union[Coin, str, dict]) -> Coin:
        if isinstance(arg, Coin):
            return arg
        elif isinstance(arg, str):
            return Coin.from_str(arg)
        else:
            return Coin.from_data(arg)

    def is_int_coin(self) -> bool:
        return isinstance(self.amount, int)

    def is_dec_coin(self) -> bool:
        return isinstance(self.amount, Dec)

    def to_int_coin(self) -> Coin:
        return Coin(self.denom, int(self.amount))

    def to_dec_coin(self) -> Coin:
        return Coin(self.denom, Dec(self.amount))

    def __str__(self) -> str:
        if self.is_dec_coin():
            amount_str = str(self.amount).rstrip("0")
            if amount_str.endswith("."):
                amount_str += "0"
            return f"{amount_str}{self.denom}"
        return f"{self.amount}{self.denom}"

    def to_data(self) -> dict:
        return {"denom": self.denom, "amount": str(self.amount)}

    @classmethod
    def from_str(cls, string: str) -> Coin:
        pattern = r"^(\-?[0-9]+(\.[0-9]+)?)([a-zA-Z]+)$"
        match = re.match(pattern, string)
        if match is None:
            raise ValueError(f"failed to parse Coin: {string}")
        else:
            return cls(match.group(3), match.group(1))

    def add(self, other: Union[Numeric.Input, Coin]) -> Coin:
        if isinstance(other, Coin):
            if other.denom != self.denom:
                raise ArithmeticError(
                    f"cannot add two Coin objects of different denoms: {self.denom} and {other.denom}"
                )
            other_amount = other.amount
        else:
            other_amount = other

        other_amount = Numeric.parse(other_amount)
        return Coin(self.denom, self.amount + other_amount)

    def __add__(self, other: Union[Numeric.Input, Coin]) -> Coin:
        return self.add(other)

    def sub(self, other: Union[Numeric.Input, Coin]) -> Coin:
        if isinstance(other, Coin):
            if other.denom != self.denom:
                raise ArithmeticError(
                    f"cannot subtract two Coin objects of different denoms: {self.denom} and {other.denom}"
                )
            other_amount = other.amount
        else:
            other_amount = other

        other_amount = Numeric.parse(other_amount)
        return Coin(self.denom, self.amount - other_amount)

    def __sub__(self, other: Union[Numeric.Input, Coin]) -> Coin:
        return self.sub(other)

    def mul(self, other: Numeric.Input) -> Coin:
        other_amount = Numeric.parse(other)
        return Coin(self.denom, self.amount * other)

    def __mul__(self, other: Numeric.Input) -> Coin:
        return self.mul(other)

    def __rmul__(self, other: Numeric.Input) -> Coin:
        return self.mul(other)

    def div(self, other: Numeric.Input) -> Coin:
        other_amount = Numeric.parse(other)
        if isinstance(other_amount, int):
            return Coin(self.denom, (self.amount // other))
        else:
            return Coin(self.denom, (self.amount / other))

    def __truediv__(self, other: Numeric.Input) -> Coin:
        return self.div(other)

    def __floordiv__(self, other: Numeric.Input) -> Coin:
        return self.div(int(Numeric.parse(other)))

    def mod(self, other: Numeric.Input) -> Coin:
        other_amount = Numeric.parse(other)
        return Coin(self.denom, self.amount % other)

    def __mod__(self, other: Numeric.Input) -> Coin:
        return self.mod(other)

    def __neg__(self) -> Coin:
        return Coin(denom=self.denom, amount=(-self.amount))

    def __abs__(self) -> Coin:
        return Coin(denom=self.denom, amount=abs(self.amount))

    def __pos__(self) -> Coin:
        return abs(self)

    @classmethod
    def from_data(cls, data: dict) -> Coin:
        return cls(data["denom"], data["amount"])
