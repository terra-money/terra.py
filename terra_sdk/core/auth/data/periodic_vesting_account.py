"""Data objects pertaining to accounts."""

from __future__ import annotations

from itertools import starmap
from typing import List

import attr
from terra_proto.cosmos.vesting.v1beta1 import Period as Period_pb
from terra_proto.cosmos.vesting.v1beta1 import (
    PeriodicVestingAccount as PeriodicVestingAccount_pb,
)

from terra_sdk.core import Coins
from terra_sdk.util.json import JSONSerializable

from ...public_key import PublicKey
from .base_account import BaseAccount
from .base_vesting_account import BaseVestingAccount

__all__ = ["Period", "PeriodicVestingAccount"]


@attr.s
class Period(JSONSerializable):
    length: int = attr.ib(converter=int)
    amount: Coins = attr.ib(converter=Coins)

    def to_amino(self) -> dict:
        return {
            "length": str(self.length),
            "amount": self.amount.to_amino(),
        }

    def to_data(self) -> dict:
        return {
            "length": str(self.length),
            "amount": self.amount.to_data(),
        }

    def to_proto(self) -> Period_pb:
        return Period_pb(length=self.length, amount=self.amount.to_proto())

    @classmethod
    def from_amino(cls, amino: dict) -> Period:
        return cls(
            length=int(amino["length"]), amount=Coins.from_amino(amino["amount"])
        )

    @classmethod
    def from_data(cls, data: dict) -> Period:
        return cls(length=data["length"], amount=Coins.from_data(data["amount"]))

    @classmethod
    def from_proto(cls, proto: Period_pb) -> Period:
        return cls(length=proto.length, amount=Coins.from_proto(proto.amount))


@attr.s
class PeriodicVestingAccount:
    """Stores information about an account with periodic vesting."""

    base_vesting_account: BaseVestingAccount = attr.ib()
    start_time: int = attr.ib()
    vesting_periods: List[Period] = attr.ib()

    type_amino = "cosmos-sdk/PeriodicVestingAccount"
    type_url = "/cosmos.vesting.v1beta1.PeriodicVestingAccount"

    def get_sequence(self) -> int:
        return self.base_vesting_account.get_sequence()

    def get_account_number(self) -> int:
        return self.base_vesting_account.get_account_number()

    def get_public_key(self) -> PublicKey:
        return self.base_vesting_account.get_public_key()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "base_vesting_account": self.base_vesting_account.to_amino(),
                "start_time": str(self.start_time),
                "vesting_periods": [vp.to_amino() for vp in self.vesting_periods],
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "base_vesting_account": self.base_vesting_account.to_data(),
            "start_time": str(self.start_time),
            "vesting_periods": [vp.to_data() for vp in self.vesting_periods],
        }

    def to_proto(self) -> PeriodicVestingAccount_pb:
        return PeriodicVestingAccount_pb(
            base_vesting_account=self.base_vesting_account.to_proto(),
            start_time=self.start_time,
            vesting_periods=[vp.to_proto for vp in self.vesting_periods],
        )

    @classmethod
    def from_amino(cls, amino: dict) -> PeriodicVestingAccount:
        amino = amino["value"]
        return cls(
            base_vesting_account=BaseVestingAccount.from_amino(
                {
                    "type": BaseVestingAccount.type_amino,
                    "value": amino["base_vesting_account"],
                }
            ),
            start_time=amino["start_time"],
            vesting_periods=[Period.from_amino(vp) for vp in amino["vesting_periods"]],
        )

    @classmethod
    def from_data(cls, data: dict) -> PeriodicVestingAccount:
        return cls(
            base_vesting_account=BaseVestingAccount.from_data(
                data["base_vesting_account"]
            ),
            start_time=data["start_time"],
            vesting_periods=[Period.from_data(vp) for vp in data["vesting_periods"]],
        )

    @classmethod
    def from_proto(cls, proto: PeriodicVestingAccount_pb) -> PeriodicVestingAccount:
        return cls(
            base_vesting_account=BaseVestingAccount.from_proto(
                proto.base_vesting_account
            ),
            start_time=proto.start_time,
            vesting_periods=[Period.from_proto(vs) for vs in proto.vesting_periods],
        )
