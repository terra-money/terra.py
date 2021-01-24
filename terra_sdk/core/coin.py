from __future__ import annotations

import attr
from .dec import Dec


@attr.s(frozen=True)
class Coin:

    denom: str = attr.ib()
    amount: int = attr.ib()

    def __repr__(self) -> str:
        return f"Coin('{self.denom}', {self.amount!r})"

    @property
    def int_coin(self) -> Coin[int]:
        return Coin(self.denom, int(self.amount))

    @property
    def dec_coin(self) -> Coin[Dec]:
        return Coin(self.denom, Dec(self.amount))

    def __str__(self) -> str:
        return f"{self.amount}{self.denom}"

    @classmethod
    def from_str(cls, string: str) -> Coin:
        pattern = r"^(\-?[0-9]+(\.[0-9]+)?)([a-zA-Z]+)$"
        match = re.match(pattern, string)
        if match:
            return cls(match.group(3), match.group(1))
        else:
            raise ValueError(f"{string} could not be parsed into Coin")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Coin):
            return self.denom == other.denom and self.amount == other.amount
        else:
            return False

    def __add__(self, other) -> Union[Coin, Coins]:
        if other == 0:
            return Coin(self.denom, self.amount)
        if isinstance(other, Coins):
            return other + self
        if not isinstance(other, Coin):
            raise TypeError(
                f"unsupported operand types for +: 'Coin' and '{type(other)}'"
            )
        if self.denom != other.denom:
            raise DenomIncompatibleError(
                f"unsupported Coin denoms for +: '{self.denom}' and '{other.denom}'"
            )
        cast = int
        if isinstance(self.amount, Dec) or isinstance(other.amount, Dec):
            cast = Dec
        return Coin(denom=self.denom, amount=cast(self.amount + other.amount))

    def __radd__(self, other) -> Union[Coin, Coins]:
        return self + other

    def __sub__(self, other: Coin) -> Coin[Union[int, Dec]]:
        if not isinstance(other, Coin):
            raise TypeError(
                f"unsupported operand types for -: 'Coin' and '{type(other)}'"
            )
        if self.denom != other.denom:
            raise DenomIncompatibleError(
                f"unsupported Coin denoms for -: '{self.denom}' and '{other.denom}'"
            )
        cast = int
        if isinstance(self.amount, Dec) or isinstance(other.amount, Dec):
            cast = Dec
        return Coin(denom=self.denom, amount=cast(self.amount - other.amount))

    def __mul__(self, other) -> Coin:
        return Coin(denom=self.denom, amount=(self.amount * other))

    def __rmul__(self, other) -> Coin:
        return self * other

    def __truediv__(self, other) -> Coin:
        cast = type(self.amount)
        return Coin(denom=self.denom, amount=cast(self.amount / other))

    def __floordiv__(self, other) -> Coin:
        cast = type(self.amount)
        return Coin(denom=self.denom, amount=cast(self.amount // other))

    def __neg__(self) -> Coin:
        return Coin(denom=self.denom, amount=(-self.amount))

    def __abs__(self) -> Coin:
        return Coin(denom=self.denom, amount=abs(self.amount))

    def __pos__(self) -> Coin:
        return abs(self)

    def __lt__(self, other: Coin) -> bool:
        if self.denom != other.denom:
            raise DenomIncompatibleError(
                f"incompatible Coin denoms for <: '{self.denom}' and '{other.denom}'"
            )
        return self.amount < other.amount

    def __gt__(self, other: Coin) -> bool:
        if self.denom != other.denom:
            raise DenomIncompatibleError(
                f"incompatible Coin denoms for >: '{self.denom}' and '{other.denom}'"
            )
        return self.amount > other.amount

    def __ge__(self, other: Coin) -> bool:
        return self > other or self == other

    def __le__(self, other: Coin) -> bool:
        return self < other or self == other

    def to_data(self) -> dict:
        return {"denom": str(self.denom), "amount": str(self.amount)}

    def _pretty_repr_(self, path="") -> str:
        return str(self)

    @classmethod
    def from_data(cls, data: Dict[str, str]) -> Coin:
        return cls(denom=data["denom"], amount=data["amount"])


class Coins:
    def __init__(self, coins: Iterable[Coin] = None, **denoms):
        if coins is None:
            coins = []
        coins = list(coins) + [Coin(d, a) for d, a in denoms.items()]
        self._cd = dict()
        for coin in list(coins):
            if self._cd.get(coin.denom, None) is None:
                self._cd[coin.denom] = Coin(coin.denom, coin.amount)
            else:
                self._cd[coin.denom] = coin + self._cd[coin.denom]

    def __repr__(self) -> str:
        rstr = ", ".join(f"{c.denom}={c.amount!r}" for c in self.coins)
        return f"Coins({rstr})"

    def __str__(self) -> str:
        return ", ".join(str(coin) for coin in self.coins)

    def to_data(self) -> List[Dict[str, str]]:
        return [coin.to_data() for coin in self.coins]

    def _pretty_repr_(self, path: str = "") -> str:
        d = terra_sdkBox({coin.denom: coin.amount for coin in self.coins})
        return d._pretty_repr_()

    def __add__(self, other: Union[Coin, Coins]) -> Coins:
        if other == 0:
            return Coins(self.coins)
        elif isinstance(other, Coins):
            return Coins(self.coins + other.coins)
        elif isinstance(other, Coin):
            return Coins(self.coins + [other])
        else:
            raise TypeError(
                f"unsupported operand types for +: 'Coins' and '{type(other)}'"
            )

    def __radd__(self, other):
        return self + other

    def __mul__(self, other: Union[int, float, Decimal, Dec]) -> Coins:
        return Coins([coin * other for coin in self.coins])

    def __rmul__(self, other) -> Coins:
        return self * other

    def __truediv__(self, other: Union[int, float, Decimal, Dec]) -> Coins:
        return Coins([coin / other for coin in self.coins])

    def __floordiv__(self, other: Union[int, float, Decimal, Dec]) -> Coins:
        return Coins([coin / other for coin in self.coins])

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Coins):
            return JsonSerializable.__eq__(self, other)
        elif isinstance(other, list):
            try:
                return JsonSerializable.__eq__(self, Coins(other))
            except AttributeError:
                return False
        else:
            return False

    @classmethod
    def from_data(cls, data: List[Dict[str, str]]) -> Coins:
        coins = map(Coin.from_data, data)
        return cls(coins)

    @property
    def denoms(self) -> List[str]:
        return sorted(self._cd.keys())

    @property
    def coins(self) -> List[Coin]:
        return sorted(self._cd.values(), key=lambda c: c.denom)

    @property
    def dec_coins(self) -> Coins:
        return Coins(c.dec_coin for c in self.coins)

    @property
    def int_coins(self) -> Coins:
        return Coins(c.int_coin for c in self.coins)

    def filter(self, predicate: Callable[[Coin], bool]) -> Coins:
        return Coins(c for c in self.coins if predicate(c))

    def __iter__(self):
        return iter(self.coins)

    def __contains__(self, denom: str) -> bool:
        return denom in self._cd

    def __getitem__(self, denom: str) -> Coin:
        return self._cd[denom]

    def __getattr__(self, name: str) -> Coin:
        if name in self.denoms:
            return self[name]
        return self.__getattribute__(name)
