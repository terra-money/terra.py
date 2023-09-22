"""Auth mdoule message types."""

from __future__ import annotations

from typing import List

from terra_proto.cosmos.vesting.v1beta1 import (
    MsgCreatePeriodicVestingAccount as MsgCreatePeriodicVestingAccount_pb,
)

from terra_sdk.core import AccAddress
from terra_sdk.core.auth.data.periodic_vesting_account import Period
from terra_sdk.core.msg import Msg

__all__ = ["MsgCreatePeriodicVestingAccount"]

import attr


@attr.s
class MsgCreatePeriodicVestingAccount(Msg):
    """MsgCreatePeriodicVestingAccount defines a message that enables creating a periodic vesting.

    Args:
        from_address (AccAddress): account to create a vesting account
        to_address (AccAddress): vesting account
        start_time (int): vesting start time
        vesting_periods (List[Period]): list of periods
    """

    type_amino = "cosmos-sdk/MsgCreatePeriodicVestingAccount"
    type_url = "/cosmos.vesting.v1beta1.MsgCreatePeriodicVestingAccount"
    prototype = MsgCreatePeriodicVestingAccount_pb

    from_address: AccAddress = attr.ib()
    to_address: AccAddress = attr.ib()
    start_time: int = attr.ib()
    vesting_periods: List[Period] = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "from_address": self.from_address,
                "to_address": self.to_address,
                "start_time": str(self.start_time),
                "vesting_periods": [vp.to_amino() for vp in self.vesting_periods],
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgCreatePeriodicVestingAccount:
        return cls(
            from_address=data["from_address"],
            to_address=data["to_address"],
            start_time=int(data["start_time"]),
            vesting_periods=[Period.from_data(vp) for vp in data["vesting_periods"]],
        )

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "from_address": self.from_address,
            "to_address": self.to_address,
            "start_time": str(self.start_time),
            "vesting_periods": [vp.to_data() for vp in self.vesting_periods],
        }

    @classmethod
    def from_proto(
        cls, proto: MsgCreatePeriodicVestingAccount_pb
    ) -> MsgCreatePeriodicVestingAccount:
        return cls(
            from_address=proto.from_address,
            to_address=proto.to_address,
            start_time=proto.start_time,
            vesting_periods=[Period.from_proto(vs) for vs in proto.vesting_periods],
        )

    def to_proto(self) -> MsgCreatePeriodicVestingAccount_pb:
        proto = MsgCreatePeriodicVestingAccount_pb()
        proto.from_address = self.from_address
        proto.to_address = self.to_address
        proto.start_time = self.start_time
        proto.vesting_periods = [vp.to_proto() for vp in self.vesting_periods]
        return proto
