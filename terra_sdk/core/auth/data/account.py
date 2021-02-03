from __future__ import annotations

from typing import List

import attr

from terra_sdk.core import Coins, PublicKey
from terra_sdk.util.json import JSONSerializable

__all__ = ["Account", "LazyGradedVestingAccount"]


@attr.s
class Account(JSONSerializable):
    """Stores information about an account fetched from the blockchain."""

    address: str = attr.ib()
    coins: Coins = attr.ib(converter=Coins)
    public_key: PublicKey = attr.ib()
    account_number: int = attr.ib(converter=int)
    sequence: int = attr.ib(converter=int)

    def to_data(self) -> dict:
        return {
            "type": "core/Account",
            "value": {
                "address": self.address,
                "coins": self.coins.to_data(),
                "public_key": self.public_key.to_data(),
                "account_number": str(self.account_number),
                "sequence": str(self.sequence),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> Account:
        data = data["value"]
        return cls(
            address=data["address"],
            coins=Coins.from_data(data["coins"]),
            public_key=PublicKey.from_data(data["public_key"]),
            account_number=data["account_number"],
            sequence=data["sequence"],
        )


@attr.s
class LazyGradedVestingAccount(Account):

    address: str = attr.ib()
    coins: Coins = attr.ib(converter=Coins)
    public_key: PublicKey = attr.ib()
    account_number: int = attr.ib(converter=int)
    sequence: int = attr.ib(converter=int)
    original_vesting: Coins = attr.ib(converter=Coins)
    delegated_free: Coins = attr.ib(converter=Coins)
    delegated_vesting: Coins = attr.ib(converter=Coins)
    end_time: int = attr.ib(converter=int)
    vesting_schedules: List[dict] = attr.ib()

    def to_data(self) -> dict:
        return {
            "type": "core/LazyGradedVestingAccount",
            "value": {
                "address": self.address,
                "coins": self.coins.to_data(),
                "public_key": self.public_key and self.public_key.to_data(),
                "account_number": str(self.account_number),
                "sequence": str(self.sequence),
                "original_vesting": self.original_vesting.to_data(),
                "delegated_free": self.delegated_free.to_data(),
                "delegated_vesting": self.delegated_vesting.to_data(),
                "end_time": str(self.end_time),
                "vesting_schedules": self.vesting_schedules,
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> LazyGradedVestingAccount:
        data = data["value"]
        return cls(
            address=data["address"],
            coins=Coins.from_data(data["coins"]),
            public_key=PublicKey.from_data(data["public_key"]),
            account_number=data["account_number"],
            sequence=data["sequence"],
            original_vesting=Coins.from_data(data["original_vesting"]),
            delegated_free=Coins.from_data(data["delegated_free"]),
            delegated_vesting=Coins.from_data(data["delegated_vesting"]),
            end_time=data["end_time"],
            vesting_schedules=data["vesting_schedules"],
        )
