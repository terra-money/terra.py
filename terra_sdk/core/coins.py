
from __future__ import annotations

from .coin import Coin

import attr

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
