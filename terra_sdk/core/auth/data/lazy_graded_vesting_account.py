"""Data objects pertaining to accounts."""

from __future__ import annotations

from typing import List

import attr
from terra_proto.terra.vesting.v1beta1 import (
    LazyGradedVestingAccount as LazyGradedVestingAccount_pb,
)

from terra_sdk.core import AccAddress, Coins

from ...public_key import PublicKey
from .base_account import BaseAccount

__all__ = ["LazyGradedVestingAccount"]


@attr.s
class LazyGradedVestingAccount(BaseAccount):
    """Stores information about an account with vesting."""

    address: AccAddress = attr.ib()
    """"""

    public_key: PublicKey = attr.ib()
    """"""

    account_number: int = attr.ib(converter=int)
    """"""

    sequence: int = attr.ib(converter=int)
    """"""

    original_vesting: Coins = attr.ib(converter=Coins)
    """"""

    delegated_free: Coins = attr.ib(converter=Coins)
    """"""

    delegated_vesting: Coins = attr.ib(converter=Coins)
    """"""

    end_time: int = attr.ib(converter=int)
    """"""

    vesting_schedules: List[dict] = attr.ib()
    """"""

    type_amino = "core/LazyGradedVestingAccount"
    type_url = "/terra.vesting.v1beta1.LazyGradedVestingAccount"

    def get_sequence(self) -> int:
        return self.sequence

    def get_account_number(self) -> int:
        return self.account_number

    def get_public_key(self) -> PublicKey:
        return self.public_key

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "address": self.address,
                "public_key": self.public_key and self.public_key.to_amino(),
                "account_number": str(self.account_number),
                "sequence": str(self.sequence),
                "original_vesting": self.original_vesting.to_amino(),
                "delegated_free": self.delegated_free.to_amino(),
                "delegated_vesting": self.delegated_vesting.to_amino(),
                "end_time": str(self.end_time),
                "vesting_schedules": self.vesting_schedules,
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "address": self.address,
            "public_key": self.public_key and self.public_key.to_data(),
            "account_number": str(self.account_number),
            "sequence": str(self.sequence),
            "original_vesting": self.original_vesting.to_data(),
            "delegated_free": self.delegated_free.to_data(),
            "delegated_vesting": self.delegated_vesting.to_data(),
            "end_time": str(self.end_time),
            "vesting_schedules": self.vesting_schedules,
        }

    @classmethod
    def from_amino(cls, amino: dict) -> LazyGradedVestingAccount:
        amino = amino["value"]
        return cls(
            address=amino["address"],
            public_key=PublicKey.from_amino(amino["public_key"])
            if amino["public_key"]
            else None,
            account_number=amino["account_number"],
            sequence=amino["sequence"],
            original_vesting=Coins.from_amino(amino["original_vesting"])
            if amino["original_vesting"]
            else None,
            delegated_free=Coins.from_amino(amino["delegated_free"])
            if amino["delegated_free"]
            else None,
            delegated_vesting=Coins.from_amino(amino["delegated_vesting"])
            if amino["delegated_vesting"]
            else None,
            end_time=amino["end_time"],
            vesting_schedules=amino["vesting_schedules"],
        )

    @classmethod
    def from_data(cls, data: dict) -> LazyGradedVestingAccount:
        return cls(
            address=data["address"],
            public_key=PublicKey.from_data(data["public_key"]),
            account_number=data["account_number"],
            sequence=data["sequence"],
            original_vesting=Coins.from_data(data["original_vesting"]),
            delegated_free=Coins.from_data(data["delegated_free"]),
            delegated_vesting=Coins.from_data(data["delegated_vesting"]),
            end_time=data["end_time"],
            vesting_schedules=data["vesting_schedules"],
        )

    def to_proto(self) -> LazyGradedVestingAccount_pb:
        proto = LazyGradedVestingAccount_pb()
        proto.base_vesting_account = self.base_vesting_account.to_proto()
        proto.vesting_schedules = [vs.to_proto() for vs in self.vesting_schedules]
        return proto
