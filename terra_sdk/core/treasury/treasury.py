from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Union

from terra_sdk.core import Coin, Dec
from terra_sdk.util.serdes import JsonDeserializable, JsonSerializable
from terra_sdk.util.validation import Schemas as S

__all__ = ["PolicyConstraints"]


@dataclass
class PolicyConstraints(JsonSerializable[dict], JsonDeserializable[dict]):

    __schema__ = S.OBJECT(
        rate_min=Dec.__schema__,
        rate_max=Dec.__schema__,
        cap=Coin.__schema__,
        change_max=Dec.__schema__,
    )

    rate_min: Dec
    rate_max: Dec
    cap: Coin
    change_max: Dec

    def clamp(self, prev_rate: Dec, new_rate: Dec):
        prev_rate = Dec(prev_rate)
        new_rate = Dec(new_rate)

        if new_rate < self.rate_min:
            new_rate = self.rate_min
        elif new_rate > self.rate_max:
            new_rate = self.rate_max

        delta = new_rate - prev_rate
        if new_rate > prev_rate:
            if delta > self.change_max:
                new_rate = prev_rate + self.change_max
        else:
            if abs(delta) > self.change_max:
                new_rate = prev_rate - self.change_max
        return new_rate

    @classmethod
    def from_data(cls, data: dict) -> PolicyConstraints:
        return cls(
            rate_min=Dec(data["rate_min"]),
            rate_max=Dec(data["rate_max"]),
            cap=Coin.from_data(data["cap"]),
            change_max=Dec(data["change_max"]),
        )
