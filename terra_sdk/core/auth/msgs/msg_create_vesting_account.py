"""Auth mdoule message types."""

from __future__ import annotations

from typing import List

from terra_proto.cosmos.vesting.v1beta1 import (
    MsgCreateVestingAccount as MsgCreateVestingAccount_pb,
)

from terra_sdk.core import AccAddress, Coins
from terra_sdk.core.msg import Msg

__all__ = ["MsgCreateVestingAccount"]

import attr


@attr.s
class MsgCreateVestingAccount(Msg):
    """MsgCreateVestingAccount defines a message that enables creating a vesting.

    Args:
        from_address (AccAddress): account to create a vesting account
        to_address (AccAddress): vesting account
        amount (Coins): vesting amount
        end_time (int): vesting end time
        delayed (bool): all coins are vested once end time is reached
    """

    type_amino = "cosmos-sdk/MsgCreateVestingAccount"
    type_url = "/cosmos.vesting.v1beta1.MsgCreateVestingAccount"
    prototype = MsgCreateVestingAccount_pb

    from_address: AccAddress = attr.ib()
    to_address: AccAddress = attr.ib()
    amount: Coins = attr.ib(converter=Coins)
    end_time: int = attr.ib()
    delayed: bool = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "from_address": self.from_address,
                "to_address": self.to_address,
                "amount": self.amount.to_amino(),
                "end_time": str(self.end_time),
                "delayed": self.delayed,
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgCreateVestingAccount:
        return cls(
            from_address=data["from_address"],
            to_address=data["to_address"],
            amount=Coins.from_data(data["amount"]),
            end_time=int(data["end_time"]),
            delayed=data["delayed"],
        )

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "from_address": self.from_address,
            "to_address": self.to_address,
            "amount": self.amount.to_data(),
            "end_time": str(self.end_time),
            "delayed": self.delayed,
        }

    @classmethod
    def from_proto(cls, proto: MsgCreateVestingAccount_pb) -> MsgCreateVestingAccount:
        return cls(
            from_address=proto.from_address,
            to_address=proto.to_address,
            amount=Coins.from_proto(proto.amount),
            end_time=proto.end_time,
            delayed=proto.delayed,
        )

    def to_proto(self) -> MsgCreateVestingAccount_pb:
        proto = MsgCreateVestingAccount_pb()
        proto.from_address = self.from_address
        proto.to_address = self.to_address
        proto.amount = [c.to_proto() for c in self.amount]
        proto.end_time = self.end_time
        proto.delayed = self.delayed
        return proto
