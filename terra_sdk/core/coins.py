from __future__ import annotations

import copy
from typing import Any, Callable, Dict, Iterable, Iterator, List, Optional, Union

from .coin import Coin
from .numeric import Numeric


class Coins:

    Input = Union[Iterable[Coin], str, Dict[str, Numeric.Input], Dict[str, Coin]]

    _coins: Dict[str, Coin]

    def __repr__(self) -> str:
        if len(self) == 0:
            return "Coins()"
        else:
            return f'Coins("{self!s}")'

    def __str__(self) -> str:
        return ",".join(str(coin) for coin in self)

    @classmethod
    def from_str(cls, s: str) -> Coins:
        coin_strings = s.split(r",")
        return Coins(Coin.from_str(cs) for cs in coin_strings)

    def __init__(self, arg: Optional[Coins.Input] = {}, **denoms):

        if arg is None:
            self._coins = {}
            return

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

        coins: Iterable[Coin]
        if isinstance(arg, dict):
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

    def get(self, denom: str) -> Optional[Coin]:
        return self._coins.get(denom)

    @classmethod
    def from_data(cls, data: list) -> Coins:
        coins = map(Coin.from_data, data)
        return cls(coins)

    def to_data(self) -> List[dict]:
        return [coin.to_data() for coin in self]

    def denoms(self) -> List[str]:
        return [c.denom for c in self]

    def to_dec_coins(self) -> Coins:
        return Coins(c.to_dec_coin() for c in self)

    def to_int_coins(self) -> Coins:
        return Coins(c.to_int_coin() for c in self)

    def add(self, other: Union[Coin, Coins]) -> Coins:
        if isinstance(other, Coin):
            return Coins([other, *self.to_list()])
        else:
            return Coins([*other.to_list(), *self.to_list()])

    def __add__(self, other: Union[Coin, Coins]) -> Coins:
        return self.add(other)

    def sub(self, other: Union[Coin, Coins]) -> Coins:
        return self.add(self.mul(-1))

    def __sub__(self, other: Union[Coin, Coins]) -> Coins:
        return self.sub(other)

    def mul(self, other: Numeric.Input) -> Coins:
        return Coins(coin.mul(other) for coin in self)

    def __mul__(self, other: Numeric.Input) -> Coins:
        return self.mul(other)

    def div(self, other: Numeric.Input) -> Coins:
        return Coins(coin.div(other) for coin in self)

    def __truediv__(self, other: Numeric.Input) -> Coins:
        return Coins(coin / other for coin in self)

    def __floordiv__(self, other: Numeric.Input) -> Coins:
        return Coins(coin // other for coin in self)

    def to_list(self) -> List[Coin]:
        return sorted(self._coins.values(), key=lambda c: c.denom)

    def filter(self, predicate: Callable[[Coin], bool]) -> Coins:
        return Coins(c for c in self if predicate(c))

    def map(self, fn: Callable[[Coin], Any]) -> Iterator[Any]:
        return map(fn, self)

    def __eq__(self, other) -> bool:
        try:
            return self.to_list() == other.to_list()
        except AttributeError:
            return False

    def __iter__(self):
        return iter(self.to_list())

    def __len__(self):
        return len(self.to_list())

    def __contains__(self, denom: str) -> bool:
        return denom in self._coins
