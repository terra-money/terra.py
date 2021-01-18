from __future__ import annotations

import re
from datetime import datetime
from decimal import Decimal

import wrapt

from terra_sdk.util.serdes import JsonDeserializable, JsonSerializable
from terra_sdk.util.validation import Schemas as S

__all__ = ["Timestamp"]


class Timestamp(wrapt.ObjectProxy, JsonSerializable, JsonDeserializable):

    # we have 2 patterns, 1 for serdes-checking in tests and 1 for checking if it works
    # python's builtin datetime
    pattern = re.compile(
        r"^(0001|[1-9]\d{3})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])T([0-1]\d|2[0-3]):([0-5]\d):([0-5]\d)(\.\d+)?Z\Z"
    )

    __schema__ = S.STRING_WITH_PATTERN(
        r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(\.\d+)?Z\Z"
    )

    def __init__(self, year, month, day, hour, minute, second, ns=0, precision=0):
        wrapt.ObjectProxy.__init__(
            self, datetime(year, month, day, hour, minute, second, ns // 1000)
        )
        self._self_ns = ns
        self._self_precision = min(9, precision)

    @property
    def ns(self):
        return self._self_ns

    @property
    def precision(self):
        return self._self_precision

    @property
    def nanosecond(self):
        return int(self.ns % 1000)

    def __str__(self) -> str:
        Y = str(self.year).rjust(4, "0")
        M = str(self.month).rjust(2, "0")
        D = str(self.day).rjust(2, "0")
        h = str(self.hour).rjust(2, "0")
        m = str(self.minute).rjust(2, "0")
        s = str(self.second).rjust(2, "0")
        r = f"{Y}-{M}-{D}T{h}:{m}:{s}"
        if self.precision > 0:
            r += "."
            r += str(self.microsecond * 1000 + self.nanosecond).rjust(9, "0")[
                : self.precision
            ]
        return r + "Z"

    def __repr__(self) -> str:
        s = self
        p = f", {s.precision}" if s.precision != 0 else ""
        return f"Timestamp({s.year}, {s.month}, {s.day}, {s.hour}, {s.minute}, {s.second}, {s.ns}{p})"

    def to_data(self) -> str:
        return str(self)

    def _pretty_repr_(self, path: str = ""):
        return self.strftime("%a %b %d '%y - %H:%M:%S.%f")

    @classmethod
    def from_datetime(cls, dt: datetime) -> Timestamp:
        return cls(
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=dt.hour,
            minute=dt.minute,
            second=dt.second,
            ns=dt.microsecond * 1000,
            precision=6 if dt.microsecond > 0 else 0,
        )

    @classmethod
    def from_data(cls, data: str) -> Timestamp:
        m = cls.pattern.match(data)
        # m = re.match(cls.__schema__["pattern"], data)
        if m:
            year, month, day, hour, minute, second = [
                int(m.group(x)) for x in range(1, 7)
            ]
            if m.group(7) is not None:
                # keep only nanosecond precision
                ns = int(Decimal(m.group(7)) * 1_000_000_000)
                precision = min(9, len(m.group(7)) - 1)
            else:
                ns = 0
                precision = 0
            return cls(year, month, day, hour, minute, second, ns, precision)
        else:
            raise ValueError(f"Timestamp could not deserialize: {data}")

    @classmethod
    def from_str(cls, string: str) -> Timestamp:
        return cls.from_data(string)

    # TODO: write datetime analogous functions for things that return datetime
    # Not sure if this is too high priority as Timestamp is not a replacement for datetime.

    def __eq__(self, other):
        if isinstance(other, Timestamp):
            return self.__wrapped__ == other.__wrapped__ and self.ns == other.ns
        return self.__wrapped__ == other and self.nanosecond == 0

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, Timestamp):
            if self.__wrapped__ == other.__wrapped__:
                return self.ns < other.ns
            else:
                return self.__wrapped__ < other.__wrapped__
        return self.__wrapped__ < other

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        if isinstance(other, Timestamp):
            if self.__wrapped__ == other.__wrapped__:
                return self.ns > other.ns
            else:
                return self.__wrapped__ > other.__wrapped__
        if self.__wrapped__ == other:
            return self.ns > 0
        else:
            return self.__wrapped__ > other

    def __ge__(self, other):
        return self == other or self > other

    # def __cmp__(self, other):
    #     if self < other:
    #         return -1
    #     elif self > other:
    #         return 1
    #     else:
    #         return 0
