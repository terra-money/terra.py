from __future__ import annotations

import attr

from terra_sdk.core.strings import AccAddress, ValAddress
from terra_sdk.util.base import BaseTerraData

__all__ = [
    "MsgModifyWithdrawAddress",
    "MsgWithdrawDelegationReward",
    "MsgWithdrawValidatorCommission",
]


@attr.s
class MsgModifyWithdrawAddress(BaseTerraData):

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
class MsgWithdrawDelegationReward(BaseTerraData):

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
class MsgWithdrawValidatorCommission(BaseTerraData):

    type = "distribution/MsgWithdrawValidatorCommission"
    action = "withdraw_validator_commission"

    validator_address: ValAddress = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgWithdrawValidatorCommission:
        data = data["value"]
        return cls(validator_address=data["validator_address"])
