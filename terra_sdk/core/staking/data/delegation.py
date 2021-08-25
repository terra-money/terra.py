from __future__ import annotations

from typing import List

import attr

from terra_sdk.core import AccAddress, Coin, Dec, ValAddress
from terra_sdk.util.json import JSONSerializable

__all__ = [
    "Delegation",
    "UnbondingDelegation",
    "UnbondingEntry",
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


@attr.s
class UnbondingEntry(JSONSerializable):
    """Contains information about an active unbonding lot of Luna."""

    initial_balance: int = attr.ib(converter=int)
    """"""
    balance: int = attr.ib(converter=int)
    """"""
    creation_height: int = attr.ib(converter=int)
    """"""
    completion_time: str = attr.ib()
    """"""

    def to_data(self) -> dict:
        return {
            "initial_balance": str(self.initial_balance),
            "balance": str(self.balance),
            "creation_height": str(self.creation_height),
            "completion_time": self.completion_time,
        }

    @classmethod
    def from_data(cls, data: dict) -> UnbondingEntry:
        return cls(
            initial_balance=data["initial_balance"],
            balance=data["balance"],
            creation_height=data["creation_height"],
            completion_time=data["completion_time"],
        )


@attr.s
class UnbondingDelegation(JSONSerializable):
    """Contains information about undelegations for a delegation pair (``delegator_address``, ``validator_address``)"""

    delegator_address: AccAddress = attr.ib()
    """"""
    validator_address: ValAddress = attr.ib()
    """"""
    entries: List[UnbondingEntry] = attr.ib()
    """"""

    @classmethod
    def from_data(cls, data) -> UnbondingDelegation:
        entries = [UnbondingEntry.from_data(entry) for entry in data["entries"]]
        return cls(
            delegator_address=data["delegator_address"],
            validator_address=data["validator_address"],
            entries=entries,
        )


@attr.s
class RedelegationEntryInfo(JSONSerializable):
    initial_balance: int = attr.ib(converter=int)
    """"""
    shares_dst: Dec = attr.ib(converter=Dec)
    """"""
    creation_height: int = attr.ib(converter=int)
    """"""
    completion_time: str = attr.ib()
    """"""


@attr.s
class RedelegationEntry(JSONSerializable):
    """Contains information about an active redelegated lot of Luna."""

    redelegation_entry: RedelegationEntryInfo = attr.ib()
    """"""
    balance: int = attr.ib(converter=int)
    """"""

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


@attr.s
class RedelegationInfo(JSONSerializable):
    delegator_address: AccAddress = attr.ib()
    """"""
    validator_src_address: ValAddress = attr.ib()
    """"""
    validator_dst_address: ValAddress = attr.ib()
    """"""


@attr.s
class Redelegation(JSONSerializable):
    """Contains informations about a redelgation for delegation tuple (``delegator_address``, ``validator_src_address``, ``validator_dst_address``)"""

    redelegation: RedelegationInfo = attr.ib()
    """"""
    entries: List[RedelegationEntry] = attr.ib()
    """"""

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
