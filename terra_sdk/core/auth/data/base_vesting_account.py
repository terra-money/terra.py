"""Data objects pertaining to accounts."""

from __future__ import annotations

import attr
from terra_proto.cosmos.vesting.v1beta1 import (
    BaseVestingAccount as BaseVestingAccount_pb,
)

from terra_sdk.core import Coins
from terra_sdk.util.json import JSONSerializable

from ...public_key import PublicKey
from .base_account import BaseAccount

__all__ = ["BaseVestingAccount"]


@attr.s
class BaseVestingAccount(JSONSerializable):
    """Stores information about an account with vesting."""

    base_account: BaseAccount = attr.ib()

    original_vesting: Coins = attr.ib(converter=Coins)
    """"""

    delegated_free: Coins = attr.ib(converter=Coins)
    """"""

    delegated_vesting: Coins = attr.ib(converter=Coins)
    """"""

    end_time: int = attr.ib(converter=int)
    """"""

    type_amino = "cosmos-sdk/BaseVestingAccount"
    type_url = "/cosmos.vesting.v1beta1.BaseVestingAccount"

    def get_sequence(self) -> int:
        return self.base_account.get_sequence()

    def get_account_number(self) -> int:
        return self.base_account.get_account_number()

    def get_public_key(self) -> PublicKey:
        return self.base_account.get_public_key()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "base_account": self.base_account.to_amino(),
                "original_vesting": self.original_vesting.to_amino(),
                "delegated_free": self.delegated_free.to_amino(),
                "delegated_vesting": self.delegated_vesting.to_amino(),
                "end_time": str(self.end_time),
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "base_account": self.base_account.to_data(),
            "original_vesting": self.original_vesting.to_data(),
            "delegated_free": self.delegated_free.to_data(),
            "delegated_vesting": self.delegated_vesting.to_data(),
            "end_time": str(self.end_time),
        }

    @classmethod
    def from_amino(cls, amino: dict) -> BaseVestingAccount:
        amino = amino["value"] if "value" in amino else amino
        return cls(
            base_account=BaseAccount.from_amino(amino["base_account"]),
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
        )

    @classmethod
    def from_data(cls, data: dict) -> BaseVestingAccount:
        return cls(
            base_account=BaseAccount.from_data(data["base_account"]),
            original_vesting=Coins.from_data(data["original_vesting"]),
            delegated_free=Coins.from_data(data["delegated_free"]),
            delegated_vesting=Coins.from_data(data["delegated_vesting"]),
            end_time=data["end_time"],
        )

    @classmethod
    def from_proto(cls, proto: BaseVestingAccount_pb) -> BaseVestingAccount:
        return cls(
            base_account=BaseAccount.from_proto(proto.base_account),
            original_vesting=Coins.from_proto(proto.original_vesting),
            delegated_free=Coins.from_proto(proto.delegated_free),
            delegated_vesting=Coins.from_proto(proto.delegated_vesting),
            end_time=proto.end_time,
        )

    def to_proto(self) -> BaseVestingAccount_pb:
        return BaseVestingAccount_pb(
            base_account=self.base_account.to_proto(),
            original_vesting=self.original_vesting.to_proto(),
            delegated_free=self.delegated_free.to_proto(),
            delegated_vesting=self.delegated_vesting.to_proto(),
            end_time=self.end_time,
        )
