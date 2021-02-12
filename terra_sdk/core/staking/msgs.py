"""Staking module message types."""

from __future__ import annotations

from typing import Optional

import attr

from terra_sdk.core import AccAddress, Coin, Dec, ValAddress, ValConsPubKey
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

    type = "staking/MsgBeginRedelegate"
    """"""
    action = "begin_redelegate"
    """"""

    delegator_address: AccAddress = attr.ib()
    validator_src_address: ValAddress = attr.ib()
    validator_dst_address: ValAddress = attr.ib()
    amount: Coin = attr.ib(converter=Coin.parse)  # type: ignore

    @classmethod
    def from_data(cls, data: dict) -> MsgBeginRedelegate:
        data = data["value"]
        return cls(
            delegator_address=data["delegator_address"],
            validator_src_address=data["validator_src_address"],
            validator_dst_address=data["validator_dst_address"],
            amount=Coin.from_data(data["amount"]),
        )


@attr.s
class MsgDelegate(Msg):
    """Delegate Luna to validator at ``validator_address``.

    Args:
        delegator_address: delegator
        validator_address: validator to delegate to
        amount (Union[str, dict, Coin]): coin (LUNA) to delegate
    """

    type = "staking/MsgDelegate"
    """"""
    action = "delegate"
    """"""

    delegator_address: AccAddress = attr.ib()
    validator_address: ValAddress = attr.ib()
    amount: Coin = attr.ib(converter=Coin.parse)  # type: ignore

    @classmethod
    def from_data(cls, data: dict) -> MsgDelegate:
        data = data["value"]
        return cls(
            delegator_address=data["delegator_address"],
            validator_address=data["validator_address"],
            amount=Coin.from_data(data["amount"]),
        )


@attr.s
class MsgUndelegate(Msg):
    """Undelegate Luna from staking position with ``validator_address``.

    Args:
        delegator_address: delegator
        validator_address: validator to undelegate from
        amount (Union[str, dict, Coin]): coin (LUNA) to undelegate
    """

    type = "staking/MsgUndelegate"
    """"""
    action = "begin_unbonding"
    """"""

    delegator_address: AccAddress = attr.ib()
    validator_address: ValAddress = attr.ib()
    amount: Coin = attr.ib(converter=Coin.parse)  # type: ignore

    @classmethod
    def from_data(cls, data: dict) -> MsgUndelegate:
        data = data["value"]
        return cls(
            delegator_address=data["delegator_address"],
            validator_address=data["validator_address"],
            amount=Coin.from_data(data["amount"]),
        )


@attr.s
class MsgEditValidator(Msg):
    """Revise validator description and configuration.

    Args:
        Description: updated validator description
        address: validator operator address
        commission_rates: new validator commission rate,
        min_self_delegation: new minimum self delegation,
    """

    type = "staking/MsgEditValidator"
    """"""
    action = "edit_validator"
    """"""

    Description: Description = attr.ib()
    address: ValAddress = attr.ib()
    commission_rate: Optional[Dec] = attr.ib(default=None)
    min_self_delegation: Optional[int] = attr.ib(default=None)

    @classmethod
    def from_data(cls, data: dict) -> MsgEditValidator:
        data = data["value"]
        msd = int(data["min_self_delegation"]) if data["min_self_delegation"] else None
        cr = Dec(data["commission_rate"]) if data["commission_rate"] else None
        return cls(
            Description=data["Description"],
            address=data["address"],
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

    type = "staking/MsgCreateValidator"
    """"""
    action = "create_validator"
    """"""

    description: Description = attr.ib()
    commission: CommissionRates = attr.ib()
    min_self_delegation: int = attr.ib()
    delegator_address: AccAddress = attr.ib()
    validator_address: ValAddress = attr.ib()
    pubkey: ValConsPubKey = attr.ib()
    value: Coin = attr.ib(converter=Coin.parse)  # type: ignore

    @classmethod
    def from_data(cls, data: dict) -> MsgCreateValidator:
        data = data["value"]
        return cls(
            description=Description.from_data(data["description"]),
            commission=CommissionRates.from_data(data["commission"]),
            min_self_delegation=int(data["min_self_delegation"]),
            delegator_address=data["delegator_address"],
            validator_address=data["validator_address"],
            pubkey=data["pubkey"],
            value=Coin.from_data(data["value"]),
        )
