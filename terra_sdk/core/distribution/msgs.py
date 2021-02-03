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

    type = "distribution/MsgModifyWithdrawAddress"
    action = "set_withdraw_address"

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

    type = "distribution/MsgWithdrawDelegationReward"
    action = "withdraw_delegation_reward"

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

    type = "distribution/MsgWithdrawValidatorCommission"
    action = "withdraw_validator_commission"

    validator_address: ValAddress = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgWithdrawValidatorCommission:
        data = data["value"]
        return cls(validator_address=data["validator_address"])


@attr.s
class MsgFundCommunityPool(Msg):

    type = "distribution/MsgFundCommunityPool"

    depositor: AccAddress = attr.ib()
    amount: Coins = attr.ib(converter=Coins)

    @classmethod
    def from_data(cls, data: dict) -> MsgFundCommunityPool:
        data = data["value"]
        return cls(depositor=data["depositor"], amount=Coins.from_data(data["amount"]))
