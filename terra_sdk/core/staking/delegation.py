from __future__ import annotations

import attr

__all__ = [
    "Delegation",
    "UnbondingDelegation",
    "UnbondingEntry",
    "Redelegation",
    "RedelegationEntry",
]


@attr.s
class Delegation(JsonSerializable, JsonDeserializable):

    delegator_address: AccAddress = attr.ib()
    validator_address: ValAddress = attr.ib()
    shares: Coin = attr.ib()
    balance: Coin = attr.ib()

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


@attr.s
class UnbondingEntry(JsonSerializable, JsonDeserializable):

    initial_balance: Coin = attr.ib()
    balance: Coin = attr.ib()
    creation_height: int = attr.ib()
    completion_time: Timestamp = attr.ib()

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


@attr.s
class UnbondingDelegation(JsonSerializable, JsonDeserializable):

    delegator_address: AccAddress = attr.ib()
    validator_address: ValAddress = attr.ib()
    entries: List[UnbondingEntry] = attr.ib()

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> UnbondingDelegation:
        entries = [UnbondingEntry.from_data(entry) for entry in data["entries"]]
        return cls(
            delegator_address=data["delegator_address"],
            validator_address=data["validator_address"],
            entries=entries,
        )


@attr.s
class RedelegationEntry(JsonSerializable, JsonDeserializable):

    initial_balance: Coin  = attr.ib()
    balance: Coin          = attr.ib()
    shares_dst: Coin       = attr.ib()
    creation_height: int   = attr.ib()
    completion_time: Timestamp = attr.ib()

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


@attr.s
class Redelegation(JsonSerializable, JsonDeserializable):

    delegator_address: AccAddress = attr.ib()
    validator_src_address: ValAddress = attr.ib()
    validator_dst_address: ValAddress = attr.ib()
    entries: List[RedelegationEntry] = attr.ib()

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> Redelegation:
        entries = [RedelegationEntry.from_data(re) for re in data["entries"]]
        return cls(
            delegator_address=data["delegator_address"],
            validator_src_address=data["validator_src_address"],
            validator_dst_address=data["validator_dst_address"],
            entries=entries,
        )
