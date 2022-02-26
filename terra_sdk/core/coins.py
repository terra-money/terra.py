from __future__ import annotations

import copy
from typing import Any, Callable, Dict, Iterable, Iterator, List, Optional, Union

from terra_proto.cosmos.base.v1beta1 import Coin as Coin_pb

from terra_sdk.util.json import JSONSerializable

from .coin import Coin
from .numeric import Numeric


class Coins(JSONSerializable, List[Coin_pb]):
    """Represents an unordered collection of :class:`Coin` objects
    -- analagous to ``sdk.Coins`` and ``sdk.DecCoins`` in Cosmos SDK. If one of the
    input coins would be ``Dec``-amount type coin, the resultant Coins is converted to
    ``Dec``-amount coins.

    Args:
        arg (Optional[Coins.Input], optional): argument to convert. Defaults to ``{}``.

    Raises:
        TypeError: if ``arg`` is not an Iterable
    """

    Input = Union[Iterable[Coin], str, Dict[str, Numeric.Input], Dict[str, Coin]]
    """Types which can be converted into a :class:`Coins` object."""

    _coins: Dict[str, Coin]

    def __repr__(self) -> str:
        if len(self) == 0:
            return "Coins()"
        else:
            return f"Coins('{self!s}')"

    def __str__(self) -> str:
        return ",".join(str(coin) for coin in self)

    @classmethod
    def from_str(cls, s: str) -> Coins:
        """Converts a comma-separated list of Coin-format strings to :class:`Coins`.

        >>> Coins.from_str('1000uluna,1234ukrw')
        Coins("1000uluna,1234ukrw")

        Args:
            s (str): string to convert
        """
        coin_strings = s.split(r",")
        return Coins(Coin.from_str(cs) for cs in coin_strings)

    def __init__(self, arg: Optional[Coins.Input] = {}, **denoms):
        """Converts the argument into a :class:`Coins` object."""

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

        # make all coins DecCoin if one is DecCoin
        if not all([c.is_int_coin() for c in self]):
            for denom in self._coins:
                self._coins[denom] = self._coins[denom].to_dec_coin()

    def __getitem__(self, denom: str) -> Coin:
        return self._coins[denom]

    def get(self, denom: str) -> Optional[Coin]:
        """Get the Coin with the denom contained in the Coins set.

        Args:
            denom (str): denom

        Returns:
            Optional[Coin]: result (can be ``None``)
        """
        return self._coins.get(denom)

    @classmethod
    def from_data(cls, data: list) -> Coins:
        """Converts list of Coin-data objects to :class:`Coins`.

        Args:
            data (list): list of Coin-data objects
        """
        coins = map(Coin.from_data, data)
        return cls(coins)

    @classmethod
    def from_amino(cls, amino: list) -> Coins:
        """Converts list of Coin-amino objects to :class:`Coins`.

        Args:
            amino (list): list of Coin-data objects
        """
        coins = map(Coin.from_amino, amino)
        return cls(coins)

    def to_amino(self) -> List[dict]:
        return [coin.to_amino() for coin in self]

    def to_data(self) -> List[dict]:
        return [coin.to_data() for coin in self]

    @classmethod
    def from_proto(cls, proto: List[Coin_pb]) -> Coins:
        """Converts list of Coin-data objects to :class:`Coins`.

        Args:
            data (list): list of Coin-data objects
        """
        coins = map(Coin.from_proto, proto)
        return cls(coins)

    def to_proto(self) -> List[Coin_pb]:
        return [coin.to_proto() for coin in self]

    def to_dict(self) -> List[dict]:
        return [coin.to_dict for coin in self]

    def denoms(self) -> List[str]:
        """Get the list of denoms for all Coin objects contained."""
        return [c.denom for c in self]

    def to_dec_coins(self) -> Coins:
        """Creates new set of :class:`Coins` that have :class`Dec` amounts."""
        return Coins(c.to_dec_coin() for c in self)

    def to_int_coins(self) -> Coins:
        """Creates new set of :class:`Coins` that have ``int`` amounts."""
        return Coins(c.to_int_coin() for c in self)

    def to_int_ceil_coins(self) -> Coins:
        """Creates a new :class:`Coins` object with all ``int`` coins with ceiling the amount"""
        return Coins(c.to_int_ceil_coin() for c in self)

    def add(self, addend: Union[Coin, Coins]) -> Coins:
        """Performs addition, which combines the sets of Coin objects. Coins of similar denoms
        will be merged into one Coin representing the denom.

        Args:
            addend (Union[Coin, Coins]): addend
        """
        if isinstance(addend, Coin):
            return Coins([addend, *self.to_list()])
        else:
            return Coins([*addend.to_list(), *self.to_list()])

    def __add__(self, addend: Union[Coin, Coins]) -> Coins:
        return self.add(addend)

    def sub(self, subtrahend: Union[Coin, Coins]) -> Coins:
        """Performs subtraction, which combines the sets of Coin objects. Coins of similar denoms
        will be merged into one Coin representing the denom.

        Args:
            subtrahend (Union[Coin, Coins]): subtrahend
        """
        return self.add(subtrahend.mul(-1))

    def __sub__(self, subtrahend: Union[Coin, Coins]) -> Coins:
        return self.sub(subtrahend)

    def mul(self, multiplier: Numeric.Input) -> Coins:
        """Performs multiplicaiton, which multiplies all the Coin objects in the set by a
        multiplier.

        Args:
            multiplier (Numeric.Input): multiplier
        """
        return Coins(coin.mul(multiplier) for coin in self)

    def __mul__(self, multiplier: Numeric.Input) -> Coins:
        return self.mul(multiplier)

    def div(self, divisor: Numeric.Input) -> Coins:
        """Performs division, which divides all the Coin objects in the set by a divisor.

        Args:
            divisor (Numeric.Input): divisor
        """
        return Coins(coin.div(divisor) for coin in self)

    def __truediv__(self, divisor: Numeric.Input) -> Coins:
        return Coins(coin / divisor for coin in self)

    def __floordiv__(self, divisor: Numeric.Input) -> Coins:
        return Coins(coin // divisor for coin in self)

    def to_list(self) -> List[Coin]:
        """Converts the set of :class:`Coin` objects contained into a sorted list by denom.

        Returns:
            List[Coin]: list, sorted by denom
        """
        return sorted(self._coins.values(), key=lambda c: c.denom)

    def filter(self, predicate: Callable[[Coin], bool]) -> Coins:
        """Creates a new :class:`Coins` collection which filters out all Coin objects that
        do not meet the predicate.

        Args:
            predicate (Callable[[Coin], bool]): predicate for filtering
        """
        return Coins(c for c in self if predicate(c))

    def map(self, fn: Callable[[Coin], Any]) -> Iterator[Any]:
        """Creates an iterable which applies the function to all coins in the set,
        ordered by denomination.

        Args:
            fn (Callable[[Coin], Any]): function to apply

        Returns:
            Iterator[Any]: coin map

        Yields:
            Iterator[Any]: coin map
        """
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
