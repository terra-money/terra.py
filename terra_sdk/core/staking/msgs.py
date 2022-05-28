"""Staking module message types."""

from __future__ import annotations

from typing import Optional

import attr
from terra_proto.cosmos.staking.v1beta1 import (
    MsgBeginRedelegate as MsgBeginRedelegate_pb,
)
from terra_proto.cosmos.staking.v1beta1 import (
    MsgCreateValidator as MsgCreateValidator_pb,
)
from terra_proto.cosmos.staking.v1beta1 import MsgDelegate as MsgDelegate_pb
from terra_proto.cosmos.staking.v1beta1 import MsgEditValidator as MsgEditValidator_pb
from terra_proto.cosmos.staking.v1beta1 import MsgUndelegate as MsgUndelegate_pb

from terra_sdk.core import AccAddress, Coin, Dec, PublicKey, ValAddress, ValConsPubKey
from terra_sdk.core.msg import Msg

from .data import CommissionRates, Description

__all__ = [
    "MsgBeginRedelegate",
    "MsgDelegate",
    "MsgUndelegate",
    "MsgEditValidator",
    "MsgCreateValidator",
]


@attr.s
class MsgBeginRedelegate(Msg):
    """Redelegate staked Luna from ``validator_src_address`` to ``valdiator_dst_address``.

    Args:
        delegator_address: delegator
        validator_src_address: validator to remove delegation FROM
        validator_dst_address: validator to transfer delegate TO
        amount (Union[str, dict, Coin]): coin (LUNA) to redelegate
    """

    type_amino = "cosmos-sdk/MsgBeginRedelegate"
    """"""
    type_url = "/cosmos.staking.v1beta1.MsgBeginRedelegate"
    """"""
    action = "begin_redelegate"
    """"""
    prototype = MsgBeginRedelegate_pb
    """"""

    delegator_address: AccAddress = attr.ib()
    validator_src_address: ValAddress = attr.ib()
    validator_dst_address: ValAddress = attr.ib()
    amount: Coin = attr.ib(converter=Coin.parse)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "delegator_address": self.delegator_address,
                "validator_src_address": self.validator_src_address,
                "validator_dst_address": self.validator_dst_address,
                "amount": self.amount.to_amino(),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgBeginRedelegate:
        return cls(
            delegator_address=data["delegator_address"],
            validator_src_address=data["validator_src_address"],
            validator_dst_address=data["validator_dst_address"],
            amount=Coin.from_data(data["amount"]),
        )

    def to_proto(self) -> MsgBeginRedelegate_pb:
        return MsgBeginRedelegate_pb(
            delegator_address=self.delegator_address,
            validator_src_address=self.validator_src_address,
            validator_dst_address=self.validator_dst_address,
            amount=self.amount.to_proto(),
        )

    @classmethod
    def from_proto(cls, proto: MsgBeginRedelegate_pb) -> MsgBeginRedelegate:
        return cls(
            delegator_address=proto.delegator_address,
            validator_src_address=proto.validator_src_address,
            validator_dst_address=proto.validator_dst_address,
            amount=Coin.from_proto(proto.amount),
        )


@attr.s
class MsgDelegate(Msg):
    """Delegate Luna to validator at ``validator_address``.

    Args:
        delegator_address: delegator
        validator_address: validator to delegate to
        amount (Union[str, dict, Coin]): coin (LUNA) to delegate
    """

    type_amino = "cosmos-sdk/MsgDelegate"
    """"""
    type_url = "/cosmos.staking.v1beta1.MsgDelegate"
    """"""
    action = "delegate"
    """"""
    prototype = MsgDelegate_pb
    """"""

    delegator_address: AccAddress = attr.ib()
    validator_address: ValAddress = attr.ib()
    amount: Coin = attr.ib(converter=Coin.parse)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "delegator_address": self.delegator_address,
                "validator_address": self.validator_address,
                "amount": self.amount.to_amino(),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgDelegate:
        return cls(
            delegator_address=data["delegator_address"],
            validator_address=data["validator_address"],
            amount=Coin.from_data(data["amount"]),
        )

    def to_proto(self) -> MsgDelegate_pb:
        return MsgDelegate_pb(
            delegator_address=self.delegator_address,
            validator_address=self.validator_address,
            amount=self.amount.to_proto(),
        )

    @classmethod
    def from_proto(cls, proto: MsgDelegate_pb) -> MsgDelegate:
        return cls(
            delegator_address=proto.delegator_address,
            validator_address=proto.validator_address,
            amount=Coin.from_proto(proto.amount),
        )


@attr.s
class MsgUndelegate(Msg):
    """Undelegate Luna from staking position with ``validator_address``.

    Args:
        delegator_address: delegator
        validator_address: validator to undelegate from
        amount (Union[str, dict, Coin]): coin (LUNA) to undelegate
    """

    type_amino = "cosmos-sdk/MsgUndelegate"
    """"""
    type_url = "/cosmos.staking.v1beta1.MsgUndelegate"
    """"""
    action = "begin_unbonding"
    """"""
    prototype = MsgUndelegate_pb
    """"""

    delegator_address: AccAddress = attr.ib()
    validator_address: ValAddress = attr.ib()
    amount: Coin = attr.ib(converter=Coin.parse)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "delegator_address": self.delegator_address,
                "validator_address": self.validator_address,
                "amount": self.amount.to_amino(),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgUndelegate:
        return cls(
            delegator_address=data["delegator_address"],
            validator_address=data["validator_address"],
            amount=Coin.from_data(data["amount"]),
        )

    def to_proto(self) -> MsgUndelegate_pb:
        return MsgUndelegate_pb(
            delegator_address=self.delegator_address,
            validator_address=self.validator_address,
            amount=self.amount.to_proto(),
        )

    @classmethod
    def from_proto(cls, proto: MsgUndelegate_pb) -> MsgUndelegate:
        return cls(
            delegator_address=proto.delegator_address,
            validator_address=proto.validator_address,
            amount=Coin.from_proto(proto.amount),
        )


@attr.s
class MsgEditValidator(Msg):
    """Revise validator description and configuration.

    Args:
        description: updated validator description
        validator_address: validator operator address
        commission_rates: new validator commission rate,
        min_self_delegation: new minimum self delegation,
    """

    type = "cosmos-sdk/MsgEditValidator"
    """"""
    type_url = "/cosmos.staking.v1beta1.MsgEditValidator"
    """"""
    action = "edit_validator"
    """"""
    prototype = MsgEditValidator_pb
    """"""

    description: Description = attr.ib()
    validator_address: ValAddress = attr.ib()
    commission_rate: Optional[Dec] = attr.ib(default=None)
    min_self_delegation: Optional[int] = attr.ib(default=None)

    @classmethod
    def from_data(cls, data: dict) -> MsgEditValidator:
        msd = int(data["min_self_delegation"]) if data["min_self_delegation"] else None
        cr = Dec(data["commission_rate"]) if data["commission_rate"] else None
        return cls(
            description=data["description"],
            validator_address=data["validator_address"],
            commission_rate=cr,
            min_self_delegation=msd,
        )

    def to_proto(self) -> MsgEditValidator_pb:
        return MsgEditValidator_pb(
            description=self.description.to_proto(),
            validator_address=self.validator_address,
            commission_rate=str(self.commission_rate) if self.commission_rate else None,
            min_self_delegation=str(self.min_self_delegation)
            if self.min_self_delegation
            else None,
        )

    @classmethod
    def from_proto(cls, proto: MsgEditValidator_pb) -> MsgEditValidator:
        msd = int(proto.min_self_delegation) if proto.min_self_delegation else "0"
        cr = Dec(proto.commission_rate) if proto.commission_rate else Dec("0")
        return cls(
            description=proto.description,
            validator_address=proto.validator_address,
            commission_rate=cr,
            min_self_delegation=msd,
        )


@attr.s
class MsgCreateValidator(Msg):
    """Register a new validator with the Terra protocol.

    Args:
        description: validator description
        commission: validator commission rates
        min_self_delegation: minimum self-delegation policy
        delegator_address: validator's account address
        validator_address: validator's operator address
        pubkey: validator consensus (Tendermint) public key
        value (Coin.Input): initial amount of Luna toi self-delegate
    """

    type = "cosmos-sdk/MsgCreateValidator"
    """"""
    type_url = "/cosmos.staking.v1beta1.MsgCreateValidator"
    """"""
    action = "create_validator"
    """"""
    prototype = MsgCreateValidator_pb
    """"""

    description: Description = attr.ib()
    commission: CommissionRates = attr.ib()
    min_self_delegation: str = attr.ib()
    delegator_address: AccAddress = attr.ib()
    validator_address: ValAddress = attr.ib()
    pubkey: ValConsPubKey = attr.ib()
    value: Coin = attr.ib(converter=Coin.parse)  # type: ignore

    @classmethod
    def from_data(cls, data: dict) -> MsgCreateValidator:
        return cls(
            description=Description.from_data(data["description"]),
            commission=CommissionRates.from_data(data["commission"]),
            min_self_delegation=int(data["min_self_delegation"]),
            delegator_address=data["delegator_address"],
            validator_address=data["validator_address"],
            pubkey=data["pubkey"],
            value=Coin.from_data(data["value"]),
        )

    def to_proto(self) -> MsgCreateValidator_pb:
        return MsgCreateValidator_pb(
            description=self.description.to_proto(),
            commission=self.commission.to_proto(),
            min_self_delegation=self.min_self_delegation,
            delegator_address=self.delegator_address,
            validator_address=self.validator_address,
            pubkey=self.pubkey.pack_any(),
            value=self.value.to_proto(),
        )

    @classmethod
    def from_proto(cls, proto: MsgCreateValidator_pb) -> MsgCreateValidator:
        return cls(
            description=Description.from_proto(proto.description),
            commission=CommissionRates.from_proto(proto.commission),
            min_self_delegation=proto.min_self_delegation,
            delegator_address=proto.delegator_address,
            validator_address=proto.validator_address,
            pubkey=PublicKey.unpack_any(proto.pubkey),
            value=Coin.from_proto(proto.value),
        )
