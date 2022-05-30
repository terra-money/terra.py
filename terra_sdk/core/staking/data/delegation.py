from __future__ import annotations

from datetime import datetime
from typing import List

import attr
from dateutil import parser
from terra_proto.cosmos.staking.v1beta1 import Delegation as Delegation_pb
from terra_proto.cosmos.staking.v1beta1 import (
    DelegationResponse as DelegationResponse_pb,
)
from terra_proto.cosmos.staking.v1beta1 import Redelegation as Redelegation_pb
from terra_proto.cosmos.staking.v1beta1 import RedelegationEntry as RedelegationEntry_pb
from terra_proto.cosmos.staking.v1beta1 import (
    RedelegationEntryResponse as RedelegationEntryResponse_pb,
)
from terra_proto.cosmos.staking.v1beta1 import (
    UnbondingDelegation as UnbondingDelegation_pb,
)
from terra_proto.cosmos.staking.v1beta1 import (
    UnbondingDelegationEntry as UnbondingDelegationEntry_pb,
)

from terra_sdk.core import AccAddress, Coin, Dec, ValAddress
from terra_sdk.util.converter import to_isoformat
from terra_sdk.util.json import JSONSerializable

__all__ = [
    "Delegation",
    "UnbondingDelegation",
    "UnbondingDelegationEntry",
    "Redelegation",
    "RedelegationEntry",
]


@attr.s
class DelegationInfo(JSONSerializable):
    delegator_address: AccAddress = attr.ib()
    validator_address: ValAddress = attr.ib()
    shares: Dec = attr.ib(converter=Dec)


@attr.s
class Delegation(JSONSerializable):
    """Contains information about a current delegation pair (``delegator_address``, ``validator_address``)"""

    delegation: DelegationInfo = attr.ib()
    balance: Coin = attr.ib(converter=Coin.parse)  # type: ignore

    def to_amino(self) -> dict:
        return {
            "delegation": {
                "delegator_address": self.delegation.delegator_address,
                "validator_address": self.delegation.validator_address,
                "shares": str(self.delegation.shares),
            },
            "balance": self.balance.to_amino(),
        }

    @classmethod
    def from_data(cls, data: dict) -> Delegation:
        return cls(
            delegation=DelegationInfo(
                delegator_address=data["delegation"]["delegator_address"],
                validator_address=data["delegation"]["validator_address"],
                shares=data["delegation"]["shares"],
            ),
            balance=Coin.from_data(data["balance"]),
        )

    def to_proto(self) -> DelegationResponse_pb:
        return DelegationResponse_pb(
            delegation=Delegation_pb(
                delegator_address=self.delegation.delegator_address,
                validator_address=self.delegation.validator_address,
                shares=str(self.delegation.shares),
            ),
            balance=self.balance.to_proto(),
        )


@attr.s
class UnbondingDelegationEntry(JSONSerializable):
    """Contains information about an active unbonding lot of Luna."""

    initial_balance: int = attr.ib(converter=int)
    """"""
    balance: int = attr.ib(converter=int)
    """"""
    creation_height: int = attr.ib(converter=int)
    """"""
    completion_time: datetime = attr.ib(converter=parser.parse)
    """"""

    def to_amino(self) -> dict:
        return {
            "initial_balance": str(self.initial_balance),
            "balance": str(self.balance),
            "creation_height": str(self.creation_height),
            "completion_time": to_isoformat(self.completion_time),
        }

    def to_data(self) -> dict:
        return {
            "initial_balance": str(self.initial_balance),
            "balance": str(self.balance),
            "creation_height": str(self.creation_height),
            "completion_time": to_isoformat(self.completion_time),
        }

    @classmethod
    def from_data(cls, data: dict) -> UnbondingDelegationEntry:
        return cls(
            initial_balance=data["initial_balance"],
            balance=data["balance"],
            creation_height=data["creation_height"],
            completion_time=data["completion_time"],
        )

    def to_proto(self) -> UnbondingDelegationEntry_pb:
        return UnbondingDelegationEntry_pb(
            initial_balance=str(self.initial_balance),
            balance=str(self.balance),
            creation_height=self.creation_height,
            completion_time=self.completion_time,
        )


@attr.s
class UnbondingDelegation(JSONSerializable):
    """Contains information about undelegations for a delegation pair (``delegator_address``, ``validator_address``)"""

    delegator_address: AccAddress = attr.ib()
    """"""
    validator_address: ValAddress = attr.ib()
    """"""
    entries: List[UnbondingDelegationEntry] = attr.ib()
    """"""

    def to_amino(self) -> dict:
        return {
            "delegator_address": self.delegator_address,
            "validator_address": self.validator_address,
            "entries": [entry.to_amino() for entry in self.entries],
        }

    @classmethod
    def from_data(cls, data: dict) -> UnbondingDelegation:
        entries = [
            UnbondingDelegationEntry.from_data(entry) for entry in data["entries"]
        ]
        return cls(
            delegator_address=data["delegator_address"],
            validator_address=data["validator_address"],
            entries=entries,
        )

    def to_proto(self) -> UnbondingDelegation_pb:
        return UnbondingDelegation_pb(
            delegator_address=self.delegator_address,
            validator_address=self.validator_address,
            entries=[entry.to_proto() for entry in self.entries],
        )


@attr.s
class RedelegationEntryInfo(JSONSerializable):
    initial_balance: int = attr.ib(converter=int)
    """"""
    shares_dst: Dec = attr.ib(converter=Dec)
    """"""
    creation_height: int = attr.ib(converter=int)
    """"""
    completion_time: datetime = attr.ib(converter=parser.parse)
    """"""

    def to_amino(self) -> dict:
        return {
            "initial_balance": str(self.initial_balance),
            "shares_dst": str(self.shares_dst),
            "creation_height": str(self.creation_height),
            "completion_time": to_isoformat(self.completion_time),
        }

    @classmethod
    def from_data(cls, data: dict) -> RedelegationEntryInfo:
        return cls(
            initial_balance=data["initial_balance"],
            shares_dst=Dec.from_data(data("shares_dst")),
            creation_height=data["creation_height"],
            completion_time=data["completion_time"],
        )

    def to_data(self) -> dict:
        return {
            "initial_balance": self.initial_balance,
            "shares_dst": self.shares_dst.to_data(),
            "creation_height": self.creation_height,
            "completion_time": to_isoformat(self.completion_time),
        }

    def to_proto(self) -> RedelegationEntry_pb:
        return RedelegationEntry_pb(
            initial_balance=str(self.initial_balance),
            shares_dst=str(self.shares_dst),
            creation_height=self.creation_height,
            completion_time=self.completion_time,
        )


@attr.s
class RedelegationEntry(JSONSerializable):
    """Contains information about an active redelegated lot of Luna."""

    redelegation_entry: RedelegationEntryInfo = attr.ib()
    """"""
    balance: int = attr.ib(converter=int)
    """"""

    def to_amino(self) -> dict:
        return {
            "redelegation_entry": self.redelegation_entry.to_amino(),
            "balance": str(self.balance),
        }

    def to_data(self) -> dict:
        return {
            "redelegation_entry": {
                "initial_balance": str(self.redelegation_entry.initial_balance),
                "shares_dst": str(self.redelegation_entry.shares_dst),
                "creation_height": self.redelegation_entry.creation_height,
                "completion_time": self.redelegation_entry.completion_time,
            },
            "balance": str(self.balance),
        }

    @classmethod
    def from_data(cls, data: dict) -> RedelegationEntry:
        return cls(
            redelegation_entry=RedelegationEntryInfo(
                initial_balance=data["redelegation_entry"]["initial_balance"],
                shares_dst=data["redelegation_entry"]["shares_dst"],
                creation_height=int(data["redelegation_entry"]["creation_height"]),
                completion_time=data["redelegation_entry"]["completion_time"],
            ),
            balance=data["balance"],
        )

    def to_proto(self) -> RedelegationEntryResponse_pb:
        return RedelegationEntryResponse_pb(
            redelegation_entry=self.redelegation_entry.to_proto(),
            balance=str(self.balance),
        )


@attr.s
class RedelegationInfo(JSONSerializable):
    delegator_address: AccAddress = attr.ib()
    """"""
    validator_src_address: ValAddress = attr.ib()
    """"""
    validator_dst_address: ValAddress = attr.ib()
    """"""

    def to_amino(self) -> dict:
        return {
            "delegator_address": self.delegator_address,
            "validator_src_address": self.validator_src_address,
            "validator_dst_address": self.validator_dst_address,
        }

    def to_data(self) -> dict:
        return {
            "delegator_address": self.delegator_address,
            "validator_src_address": self.validator_src_address,
            "validator_dst_address": self.validator_dst_address,
        }

    @classmethod
    def from_data(cls, data: dict) -> RedelegationInfo:
        return cls(
            delegator_address=data["delegator_address"],
            validator_src_address=data["validator_src_address"],
            validator_dst_address=data["validator_dst_address"],
        )

    def to_proto(self) -> Redelegation_pb:
        return Redelegation_pb(
            delegator_address=self.delegator_address,
            validator_src_address=self.validator_src_address,
            validator_dst_address=self.validator_dst_address,
        )


@attr.s
class Redelegation(JSONSerializable):
    """Contains informations about a redelgation for delegation tuple (``delegator_address``, ``validator_src_address``, ``validator_dst_address``)"""

    redelegation: RedelegationInfo = attr.ib()
    """"""
    entries: List[RedelegationEntry] = attr.ib()
    """"""

    def to_amino(self) -> dict:
        return {
            "redelegation": self.redelegation.to_amino(),
            "entries": [entry.to_amino() for entry in self.entries],
        }

    @classmethod
    def from_data(cls, data: dict) -> Redelegation:
        entries = [RedelegationEntry.from_data(re) for re in data["entries"]]
        return cls(
            redelegation=RedelegationInfo(
                delegator_address=data["redelegation"]["delegator_address"],
                validator_src_address=data["redelegation"]["validator_src_address"],
                validator_dst_address=data["redelegation"]["validator_dst_address"],
            ),
            entries=entries,
        )

    def to_proto(self) -> Redelegation_pb:
        return Redelegation_pb(
            delegator_address=self.redelegation.delegator_address,
            validator_src_address=self.redelegation.validator_src_address,
            validator_dst_address=self.redelegation.validator_dst_address,
            entries=[entry.to_proto() for entry in self.entries],
        )
