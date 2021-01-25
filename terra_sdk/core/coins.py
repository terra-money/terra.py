from __future__ import annotations

from .coin import Coin
import copy
from typing import Dict

import attr


class Coins:

    _coins: Dict[str, Coin]

    def __str__(self) -> str:
        return ",".join(str(coin) for coin in self.coins)

    @classmethod
    def from_str(cls, s: str) -> Coins:
        coin_strings = s.split(r",\s")

    def __init__(self, arg: Coins.Input = {}, **denoms):
        if isinstance(args, Coins):
            self._coins = copy.deepcopy(arg._coins)
        elif isinstance(args, str):
            self._coins = Coins.from_string(arg)._coins
        elif isinstance(args, dict) or isinstance(args, set):
            coins = [Coin(denom, arg[denom]) for denom in args]
        else:
            try:
                iter(arg)
            except TypeError:
                raise TypeError(f"could not create Coins object with argument: {arg}")
            coins = arg  # expect args to be Iterable[Coin]
        self._coins = Coins(denoms)._coins
        for coin in coins:
            x = _coins.get(coin.denom)
            if x is not None:
                self._coins[coin.denom] = x + coin
            else:
                self._coins[coin.denom] = coin

        # check the
        if not all([c.is_dec_coin() for c in self]) and not all(
            [c.is_int_coin() for c in self]
        ):
            raise TypeError(
                f"non-homogenous instantiation of Coins not supported: {self:s}"
            )

    def __getitem__(self, denom: str) -> Coin:
        return self._cd[denom]

    @classmethod
    def from_data(cls, data: List[Dict[str, str]]) -> Coins:
        coins = map(Coin.from_data, data)
        return cls(coins)

    def to_data(self) -> List[Dict[str, str]]:
        return [coin.to_data() for coin in self.coins]

    def denoms(self) -> str:
        return [c.denom for c in self]

    def to_dec_coins(self) -> Coins:
        return Coins([c.to_dec_coin() for c in self])

    def to_int_coins(self) -> Coins:
        return Coins([c.to_int_coin() for c in self])

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

    @property
    def coins(self) -> List[Coin]:
        return sorted(self._cd.values(), key=lambda c: c.denom)

    def filter(self, predicate: Callable[[Coin], bool]) -> Coins:
        return Coins(c for c in self.coins if predicate(c))

    def __iter__(self):
        return iter(self.coins)

    def __contains__(self, denom: str) -> bool:
        return denom in self._cd
