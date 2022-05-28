"""Data objects pertaining to accounts."""

from __future__ import annotations

from itertools import starmap
from typing import List

import attr
from terra_proto.cosmos.vesting.v1beta1 import (
    ContinuousVestingAccount as ContinuousVestingAccount_pb,
)

from terra_sdk.core import Dec
from terra_sdk.util.json import JSONSerializable

from ...public_key import PublicKey
from .base_account import BaseAccount
from .base_vesting_account import BaseVestingAccount

__all__ = ["ContinuousVestingAccount"]


@attr.s
class ContinuousVestingAccount:
    """Stores information about an account with continuous vesting."""

    base_vesting_account: BaseVestingAccount = attr.ib()
    start_time: int = attr.ib()

    type_amino = "cosmos-sdk/ContinuousVestingAccount"
    type_url = "/cosmos.vesting.v1beta1.ContinuousVestingAccount"

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
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "base_vesting_account": self.base_vesting_account.to_data(),
            "start_time": str(self.start_time),
        }

    def to_proto(self) -> ContinuousVestingAccount_pb:
        return ContinuousVestingAccount_pb(
            base_vesting_account=self.base_vesting_account.to_proto(),
            start_time=self.start_time,
        )

    @classmethod
    def from_amino(cls, amino: dict) -> ContinuousVestingAccount:
        amino = amino["value"]
        return cls(
            base_vesting_account=BaseVestingAccount.from_amino(
                amino["base_vesting_account"]
            ),
            start_time=amino["start_time"],
        )

    @classmethod
    def from_data(cls, data: dict) -> ContinuousVestingAccount:
        return cls(
            base_vesting_account=BaseVestingAccount.from_data(
                data["base_vesting_account"]
            ),
            start_time=data["start_time"],
        )

    @classmethod
    def from_proto(cls, proto: ContinuousVestingAccount_pb) -> ContinuousVestingAccount:
        return cls(
            base_vesting_account=BaseVestingAccount.from_proto(
                proto.base_vesting_account
            ),
            start_time=proto.start_time,
        )
