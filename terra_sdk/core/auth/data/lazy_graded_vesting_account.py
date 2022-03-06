"""Data objects pertaining to accounts."""

from __future__ import annotations

from typing import List

import attr
from terra_proto.terra.vesting.v1beta1 import (
    LazyGradedVestingAccount as LazyGradedVestingAccount_pb,
)
from terra_proto.terra.vesting.v1beta1 import Schedule as Schedule_pb
from terra_proto.terra.vesting.v1beta1 import VestingSchedule as VestingSchedule_pb

from terra_sdk.core import Dec
from terra_sdk.util.json import JSONSerializable

from ...public_key import PublicKey
from .base_account import BaseAccount
from .base_vesting_account import BaseVestingAccount

__all__ = ["Schedule", "VestingSchedule", "LazyGradedVestingAccount"]


@attr.s
class Schedule(JSONSerializable):
    start_time: int = attr.ib(converter=int)
    end_time: int = attr.ib(converter=int)
    ratio: Dec = attr.ib()

    def to_data(self) -> dict:
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "ratio": self.ratio,
        }

    def to_amino(self) -> dict:
        return {
            "start_time": str(self.start_time),
            "end_time": str(self.end_time),
            "ratio": str(self.ratio),
        }

    def to_proto(self) -> Schedule_pb:
        return Schedule_pb(
            start_time=self.start_time, end_time=self.end_time, ratio=str(self.ratio)
        )

    @classmethod
    def from_data(cls, data: dict) -> Schedule:
        return cls(
            start_time=data["start_time"],
            end_time=data["end_time"],
            ratio=Dec.from_data(data["ratio"]),
        )

    @classmethod
    def from_amino(cls, amino: dict) -> Schedule:
        return cls(
            start_time=int(amino["start_time"]),
            end_time=int(amino["end_time"]),
            ratio=Dec(amino["ratio"]),
        )

    @classmethod
    def from_proto(cls, proto: Schedule_pb) -> Schedule:
        return cls(
            start_time=proto.start_time, end_time=proto.end_time, ratio=Dec(proto.ratio)
        )


@attr.s
class VestingSchedule(JSONSerializable):
    denom: str = attr.ib()
    schedules: List[Schedule] = attr.ib()

    def to_data(self) -> dict:
        return {
            "denom": self.denom,
            "schedules": [sch.to_data() for sch in self.schedules],
        }

    def to_amino(self) -> dict:
        return {
            "denom": self.denom,
            "schedules": [sch.to_amino() for sch in self.schedules],
        }

    def to_proto(self) -> VestingSchedule_pb:
        return VestingSchedule_pb(
            denom=self.denom, schedules=[sch.to_proto() for sch in self.schedules]
        )

    @classmethod
    def from_data(cls, data: dict) -> VestingSchedule:
        return cls(
            denom=data["denom"],
            schedules=[Schedule.from_data(sch) for sch in data["schedules"]],
        )

    @classmethod
    def from_amino(cls, amino: dict) -> VestingSchedule:
        return cls(
            denom=amino["denom"],
            schedules=[Schedule.from_amino(sch) for sch in amino["schedules"]],
        )

    @classmethod
    def from_proto(cls, proto: VestingSchedule_pb) -> VestingSchedule:
        return cls(
            denom=proto.denom,
            schedules=[Schedule.from_proto(sch) for sch in proto.schedules],
        )


@attr.s
class LazyGradedVestingAccount(BaseAccount):
    """Stores information about an account with lazy graded vesting."""

    base_vesting_account: BaseVestingAccount = attr.ib()
    vesting_schedules: List[VestingSchedule] == attr.ib()

    type_amino = "core/LazyGradedVestingAccount"
    type_url = "/terra.vesting.v1beta1.LazyGradedVestingAccount"

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
                "vesting_schedules": [vs.to_amino() for vs in self.vesting_schedules],
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "base_vesting_account": self.base_vesting_account.to_data(),
            "vesting_schedules": [vs.to_data() for vs in self.vesting_schedules],
        }

    @classmethod
    def from_amino(cls, amino: dict) -> LazyGradedVestingAccount:
        amino = amino["value"]
        return cls(
            base_vesting_account=BaseVestingAccount.from_amino(
                amino["base_vesting_account"]
            ),
            vesting_schedules=[
                VestingSchedule.from_amino(vs) for vs in amino["vesting_schedules"]
            ],
        )

    @classmethod
    def from_data(cls, data: dict) -> LazyGradedVestingAccount:
        return cls(
            base_vesting_account=BaseVestingAccount.from_data(
                data["base_vesting_account"]
            ),
            vesting_schedules=[
                VestingSchedule.from_data(vs) for vs in data["vesting_schedules"]
            ],
        )

    @classmethod
    def from_proto(cls, proto: LazyGradedVestingAccount_pb) -> LazyGradedVestingAccount:
        return cls(
            base_vesting_account=BaseVestingAccount.from_proto(
                proto.base_vesting_account
            ),
            vesting_schedules=[
                VestingSchedule.from_proto(vs) for vs in proto["vesting_schedules"]
            ],
        )

    def to_proto(self) -> LazyGradedVestingAccount_pb:
        return LazyGradedVestingAccount_pb(
            base_vesting_account=self.base_vesting_account.to_proto(),
            vesting_schedules=[vs.to_proto() for vs in self.vesting_schedules],
        )
