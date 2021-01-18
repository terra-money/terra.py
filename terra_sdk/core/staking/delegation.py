from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from terra_sdk.core import AccAddress, Coin, Dec, Timestamp, ValAddress
from terra_sdk.core.denoms import uLuna
from terra_sdk.util.serdes import JsonDeserializable, JsonSerializable
from terra_sdk.util.validation import Schemas as S

__all__ = [
    "Delegation",
    "UnbondingDelegation",
    "UnbondingEntry",
    "Redelegation",
    "RedelegationEntry",
]


@dataclass
class Delegation(JsonSerializable, JsonDeserializable):

    delegator_address: AccAddress
    validator_address: ValAddress
    shares: Coin
    balance: Coin

    def to_data(self) -> dict:
        return {
            "delegator_address": self.delegator_address,
            "validator_address": self.validator_address,
            "shares": str(self.shares.amount),
            "balance": str(self.balance.amount),
        }

    @classmethod
    def from_data(cls, data: Dict[str, str]) -> Delegation:
        return cls(
            delegator_address=data["delegator_address"],
            validator_address=data["validator_address"],
            shares=Coin(uLuna, data["shares"]),
            balance=Coin(uLuna, data["balance"]),
        )


@dataclass
class UnbondingEntry(JsonSerializable, JsonDeserializable):

    initial_balance: Coin
    balance: Coin
    creation_height: int
    completion_time: Timestamp

    def to_data(self) -> dict:
        return {
            "initial_balance": str(self.initial_balance.amount),
            "balance": str(self.balance.amount),
            "creation_height": str(self.creation_height),
            "completion_time": self.completion_time,
        }

    @classmethod
    def from_data(cls, data: Dict[str, str]) -> UnbondingEntry:
        return cls(
            initial_balance=Coin(uLuna, data["initial_balance"]),
            balance=Coin(uLuna, data["balance"]),
            creation_height=int(data["creation_height"]),
            completion_time=Timestamp.from_data(data["completion_time"]),
        )


@dataclass
class UnbondingDelegation(JsonSerializable, JsonDeserializable):

    delegator_address: AccAddress
    validator_address: ValAddress
    entries: List[UnbondingEntry]

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> UnbondingDelegation:
        entries = [UnbondingEntry.from_data(entry) for entry in data["entries"]]
        return cls(
            delegator_address=data["delegator_address"],
            validator_address=data["validator_address"],
            entries=entries,
        )


@dataclass
class RedelegationEntry(JsonSerializable, JsonDeserializable):

    initial_balance: Coin
    balance: Coin
    shares_dst: Coin
    creation_height: int
    completion_time: Timestamp

    def to_data(self) -> dict:
        return {
            "creation_height": self.creation_height,
            "completion_time": self.completion_time,
            "initial_balance": str(self.initial_balance.amount),
            "balance": str(self.balance.amount),
            "shares_dst": str(self.shares_dst.amount),
        }

    @classmethod
    def from_data(cls, data: dict) -> RedelegationEntry:
        return cls(
            initial_balance=Coin(uLuna, data["initial_balance"]),
            balance=Coin(uLuna, data["balance"]),
            shares_dst=Coin(uLuna, data["shares_dst"]),
            creation_height=int(data["creation_height"]),
            completion_time=Timestamp.from_data(data["completion_time"]),
        )


@dataclass
class Redelegation(JsonSerializable, JsonDeserializable):

    delegator_address: AccAddress
    validator_src_address: ValAddress
    validator_dst_address: ValAddress
    entries: List[RedelegationEntry]

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> Redelegation:
        entries = [RedelegationEntry.from_data(re) for re in data["entries"]]
        return cls(
            delegator_address=data["delegator_address"],
            validator_src_address=data["validator_src_address"],
            validator_dst_address=data["validator_dst_address"],
            entries=entries,
        )
