from __future__ import annotations

from terra_sdk.util.base import BaseTerraData

__all__ = ["PolicyConstraints"]


@attr.s
class PolicyConstraints(BaseTerraData):

    rate_min: Dec = attr.ib()
    rate_max: Dec = attr.ib()
    cap: Coin = attr.ib()
    change_max: Dec = attr.ib()

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
