from __future__ import annotations

import attr

from terra_sdk.core import Dec, Coin, AccAddress, ValAddress

__all__ = [
    "Delegation",
    "UnbondingDelegation",
    "UnbondingEntry",
    "Redelegation",
    "RedelegationEntry",
]


@attr.s
class Delegation:

    delegator_address: AccAddress = attr.ib()
    validator_address: ValAddress = attr.ib()
    shares: Dec = attr.ib(converter=Dec)
    balance: Coin = attr.ib(converter=Coin.parse)

    def to_data(self) -> dict:
        return {
            "delegator_address": self.delegator_address,
            "validator_address": self.validator_address,
            "shares": str(self.shares),
            "balance": self.balance.to_data(),
        }

    @classmethod
    def from_data(cls, data: dict) -> Delegation:
        return cls(
            delegator_address=data["delegator_address"],
            validator_address=data["validator_address"],
            shares=data["shares"],
            balance=data["balance"],
        )


@attr.s
class UnbondingEntry:

    initial_balance: int = attr.ib(converter=int)
    balance: int = attr.ib(converter=int)
    creation_height: int = attr.ib(converter=int)
    completion_time: str = attr.ib()

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
class UnbondingDelegation:

    delegator_address: AccAddress = attr.ib()
    validator_address: ValAddress = attr.ib()
    entries: List[UnbondingEntry] = attr.ib()

    def to_data(self) -> dict:
        return {
            "delegator_address": self.delegator_address,
            "validator_address": self.validator_address,
            "entries": [ue.to_data() for ue in self.entries],
        }

    @classmethod
    def from_data(cls, data) -> UnbondingDelegation:
        entries = [UnbondingEntry.from_data(entry) for entry in data["entries"]]
        return cls(
            delegator_address=data["delegator_address"],
            validator_address=data["validator_address"],
            entries=entries,
        )


@attr.s
class RedelegationEntry:

    initial_balance: int = attr.ib(converter=int)
    balance: int = attr.ib(converter=int)
    shares_dst: Dec = attr.ib(converter=Dec)
    creation_height: int = attr.ib(converter=int)
    completion_time: str = attr.ib()

    def to_data(self) -> dict:
        return {
            "creation_height": self.creation_height,
            "completion_time": self.completion_time,
            "initial_balance": str(self.initial_balance),
            "balance": str(self.balance),
            "shares_dst": str(self.shares_dst),
        }

    @classmethod
    def from_data(cls, data: dict) -> RedelegationEntry:
        return cls(
            initial_balance=data["initial_balance"],
            balance=data["balance"],
            shares_dst=data["shares_dst"],
            creation_height=int(data["creation_height"]),
            completion_time=data["completion_time"],
        )


@attr.s
class Redelegation:

    delegator_address: AccAddress = attr.ib()
    validator_src_address: ValAddress = attr.ib()
    validator_dst_address: ValAddress = attr.ib()
    entries: List[RedelegationEntry] = attr.ib()

    def to_data(self) -> dict:
        return {
            "delegator_address": self.delegator_address,
            "validator_src_address": self.validator_src_address,
            "validator_dst_address": self.validator_dst_address,
            "entries": [re.to_data() for re in self.entries],
        }

    @classmethod
    def from_data(cls, data: dict) -> Redelegation:
        entries = [RedelegationEntry.from_data(re) for re in data["entries"]]
        return cls(
            delegator_address=data["delegator_address"],
            validator_src_address=data["validator_src_address"],
            validator_dst_address=data["validator_dst_address"],
            entries=entries,
        )
