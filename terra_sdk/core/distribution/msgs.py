"""Distribution module message types."""

from __future__ import annotations

import attr

from terra_sdk.core import AccAddress, Coins, ValAddress
from terra_sdk.core.msg import Msg

__all__ = [
    "MsgModifyWithdrawAddress",
    "MsgWithdrawDelegationReward",
    "MsgWithdrawValidatorCommission",
    "MsgFundCommunityPool",
]


@attr.s
class MsgModifyWithdrawAddress(Msg):
    """Modify the Withdraw Address of a delegator.

    Args:
        delegator_address: delegator
        withdraw_address: new withdraw address
    """

    type = "distribution/MsgModifyWithdrawAddress"
    """"""
    action = "set_withdraw_address"
    """"""

    delegator_address: AccAddress = attr.ib()
    withdraw_address: AccAddress = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgModifyWithdrawAddress:
        data = data["value"]
        return cls(
            delegator_address=data["delegator_address"],
            withdraw_address=data["withdraw_address"],
        )


@attr.s
class MsgWithdrawDelegationReward(Msg):
    """Withdraw rewards for a delegation specified by a (delegator, validator) pair.

    Args:
        delegator_address: delegator
        validator_address: validator
    """

    type = "distribution/MsgWithdrawDelegationReward"
    """"""
    action = "withdraw_delegation_reward"
    """"""

    delegator_address: AccAddress = attr.ib()
    validator_address: ValAddress = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgWithdrawDelegationReward:
        data = data["value"]
        return cls(
            delegator_address=data["delegator_address"],
            validator_address=data["validator_address"],
        )


@attr.s
class MsgWithdrawValidatorCommission(Msg):
    """Withdraw rewards accrued for a validator gained through commissions.

    Args:
        validator_address: validator operator address
    """

    type = "distribution/MsgWithdrawValidatorCommission"
    """"""
    action = "withdraw_validator_commission"
    """"""

    validator_address: ValAddress = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgWithdrawValidatorCommission:
        data = data["value"]
        return cls(validator_address=data["validator_address"])


@attr.s
class MsgFundCommunityPool(Msg):
    """Deposit assets to the Community Pool.

    Args:
        depositor (AccAddress): sender
        amount (Coins): amount to fund community pool with
    """

    type = "distribution/MsgFundCommunityPool"
    """"""

    depositor: AccAddress = attr.ib()
    amount: Coins = attr.ib(converter=Coins)

    @classmethod
    def from_data(cls, data: dict) -> MsgFundCommunityPool:
        data = data["value"]
        return cls(depositor=data["depositor"], amount=Coins.from_data(data["amount"]))
