from __future__ import annotations

import attr
from .dec import Dec


@attr.s(frozen=True)
class Coin:

    denom: str = attr.ib()
    amount: int = attr.ib()

    def is_int_coin(self) -> bool:
        return isinstance(self.amount, int)

    def is_dec_coin(self) -> bool:
        return isinstance(self.amount, Dec)

    def to_int_coin(self) -> Coin:
        return Coin(self.denom, int(self.amount))

    def to_dec_coin(self) -> Coin:
        return Coin(self.denom, Dec(self.amount))

    def __str__(self) -> str:
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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Coin):
            return self.denom == other.denom and self.amount == other.amount
        else:
            return False

    def __add__(self, other: Union[Numeric.Input, Coin]) -> Coin:
        if isinstance(other, Coin):
            if other.denom !== self.denom:
                raise ArithmeticError(f"cannot add two Coin objects of different denoms: {self.denom} and {other.denom}")
            other_amount = other.amount
        else:
            other_amount = other
        
        other_amount = Numeric.parse(other_amount)
        return Coin(self.denom, self.amount + other_amount)
        
    def __sub__(self, other: Union[Numeric.Input, Coin]) -> Coin:
        if isinstance(other, Coin):
            if other.denom !== self.denom:
                raise ArithmeticError(f"cannot subtract two Coin objects of different denoms: {self.denom} and {other.denom}")
            other_amount = other.amount
        else:
            other_amount = other
        
        other_amount = Numeric.parse(other_amount)
        return Coin(self.denom, self.amount - other_amount)

    def __mul__(self, other: Numeric.Input) -> Coin:
        other_amount = Numeric.parse(other)
        return Coin(self.denom, self.amount * other)

    def __rmul__(self, other) -> Coin:
        return self * other

    def __truediv__(self, other) -> Coin:
        other_amount = Numeric.parse(other)
        return Coin(self.denom, (self.amount / other))
    
    def __floordiv__(self, other) -> Coin:
        other_amount = Numeric.parse(other)
        return Coin(self.denom, (self.amount // other))
    
    def __mod__(self, other) -> Coin:
        other_amount = Numeric.parse(other)
        return Coin(self.denom, self.amount % other)

    def __neg__(self) -> Coin:
        return Coin(denom=self.denom, amount=(-self.amount))

    def __abs__(self) -> Coin:
        return Coin(denom=self.denom, amount=abs(self.amount))

    def __pos__(self) -> Coin:
        return abs(self)

    @classmethod
    def from_data(cls, data: dict) -> Coin:
        return cls(data["denom"], data["amount"])
