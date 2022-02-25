"""Treasury module data objects."""

from __future__ import annotations

__all__ = ["PolicyConstraints"]

import attr
from terra_proto.terra.treasury.v1beta1 import PolicyConstraints as PolicyConstraints_pb

from terra_sdk.core import Coin, Dec


@attr.s
class PolicyConstraints:
    """Contains information about tax reward or reward weight
    policy constraints.
    """

    rate_min: Dec = attr.ib()
    """"""
    rate_max: Dec = attr.ib()
    """"""
    cap: Coin = attr.ib()
    """"""
    change_rate_max: Dec = attr.ib()
    """"""

    def clamp(self, prev_rate: Dec, new_rate: Dec) -> Dec:
        """Simulates the effect of the policy contraint.

        Args:
            prev_rate (Dec): previous rate
            new_rate (Dec): new rate

        Returns:
            Dec: result of clamp (constrained change)
        """
        prev_rate = Dec(prev_rate)
        new_rate = Dec(new_rate)

        if new_rate < self.rate_min:
            new_rate = self.rate_min
        elif new_rate > self.rate_max:
            new_rate = self.rate_max

        delta = new_rate - prev_rate
        if new_rate > prev_rate:
            if delta > self.change_rate_max:
                new_rate = prev_rate + self.change_rate_max
        else:
            if abs(delta) > self.change_rate_max:
                new_rate = prev_rate - self.change_rate_max
        return new_rate

    def to_amino(self) -> dict:
        return {
            "rate_min": str(self.rate_min),
            "rate_max": str(self.rate_max),
            "cap": self.cap.to_amino(),
            "change_rate_max": str(self.change_rate_max)
        }

    @classmethod
    def from_data(cls, data: dict) -> PolicyConstraints:
        return cls(
            rate_min=Dec(data["rate_min"]),
            rate_max=Dec(data["rate_max"]),
            cap=Coin.from_data(data["cap"]),
            change_rate_max=Dec(data["change_rate_max"]),
        )

    def to_proto(self) -> PolicyConstraints_pb:
        return PolicyConstraints_pb(
            rate_min=str(self.rate_min),
            rate_max=str(self.rate_max),
            cap=self.cap.to_proto(),
            change_rate_max=str(self.change_rate_max),
        )
