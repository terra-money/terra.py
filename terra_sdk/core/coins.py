from __future__ import annotations

from typing import Dict, Iterable, Union
import copy

from .coin import Coin
from .numeric import Numeric

import attr


class Coins:

    Input = Union[Iterable[Coin], str, Dict[str, Numeric.Input], Dict[str, Coin]]

    _coins: Dict[str, Coin]

    def __str__(self) -> str:
        return ",".join(str(coin) for coin in self)

    @classmethod
    def from_str(cls, s: str) -> Coins:
        coin_strings = s.split(r",\s")
        return Coins(Coin.from_str(cs) for cs in coin_strings)

    def __init__(self, arg: Coins.Input = {}, **denoms):

        # arg should be an iterable
        try:
            iter(arg)
        except TypeError:
            raise TypeError(f"could not create Coins object with argument: {arg!s}")

        if isinstance(arg, Coins):
            self._coins = copy.deepcopy(arg._coins)
            return

        if isinstance(arg, str):
            self._coins = Coins.from_str(arg)._coins
            return

        self._coins = Coins(denoms)._coins if denoms else {}
        if isinstance(arg, dict) or isinstance(arg, set):
            coins = [Coin(denom, arg[denom]) for denom in arg]
        else:
            coins = arg
        for coin in coins:
            x = self._coins.get(coin.denom)
            if x is not None:
                self._coins[coin.denom] = x + coin
            else:
                self._coins[coin.denom] = coin

        # check homogeneous
        if not all([c.is_dec_coin() for c in self]) and not all(
            [c.is_int_coin() for c in self]
        ):
            raise TypeError(
                f"non-homogenous instantiation of Coins not supported: {self!s}"
            )

    def __getitem__(self, denom: str) -> Coin:
        return self._coins[denom]

    @classmethod
    def from_data(cls, data: list) -> Coins:
        coins = map(Coin.from_data, data)
        return cls(coins)

    def to_data(self) -> list:
        return [coin.to_data() for coin in self]

    def denoms(self) -> str:
        return [c.denom for c in self]

    def to_dec_coins(self) -> Coins:
        return Coins(c.to_dec_coin() for c in self)

    def to_int_coins(self) -> Coins:
        return Coins(c.to_int_coin() for c in self)

    def mul(self, other: Numeric.Input) -> Coins:
        return Coins(coin.mul(other) for coin in self)

    def __truediv__(self, other: Numeric.Input) -> Coins:
        return Coins(coin.div(other) for coin in self)

    def to_list(self) -> List[Coin]:
        return sorted(self._coins.values(), key=lambda c: c.denom)

    def filter(self, predicate: Callable[[Coin], bool]) -> Coins:
        return Coins(c for c in self if predicate(c))

    def map(self, fn: Callable[[Coin], bool]) -> Map[Coin]:
        return map(fn, self)

    def __iter__(self):
        return iter(self.to_list())

    def __contains__(self, denom: str) -> bool:
        return denom in self._coins
