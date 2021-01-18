from __future__ import annotations

from dataclasses import dataclass

from terra_sdk.core import AccAddress, ValAddress
from terra_sdk.core.msg import StdMsg
from terra_sdk.util.validation import Schemas as S
from terra_sdk.util.validation import validate_acc_address, validate_val_address

__all__ = [
    "MsgModifyWithdrawAddress",
    "MsgWithdrawDelegationReward",
    "MsgWithdrawValidatorCommission",
]


@dataclass
class MsgModifyWithdrawAddress(StdMsg):

    type = "distribution/MsgModifyWithdrawAddress"
    action = "set_withdraw_address"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^distribution/MsgModifyWithdrawAddress\Z"),
        value=S.OBJECT(delegator_address=S.ACC_ADDRESS, withdraw_address=S.ACC_ADDRESS),
    )

    delegator_address: AccAddress
    withdraw_address: AccAddress

    def __post_init__(self):
        self.delegator_address = validate_acc_address(self.delegator_address)
        self.withdraw_address = validate_acc_address(self.withdraw_address)

    @classmethod
    def from_data(cls, data: dict) -> MsgModifyWithdrawAddress:
        data = data["value"]
        return cls(
            delegator_address=data["delegator_address"],
            withdraw_address=data["withdraw_address"],
        )


@dataclass
class MsgWithdrawDelegationReward(StdMsg):

    type = "distribution/MsgWithdrawDelegationReward"
    action = "withdraw_delegation_reward"

    schema = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^distribution/MsgWithdrawDelegationReward\Z"),
        value=S.OBJECT(
            delegator_address=S.ACC_ADDRESS, validator_address=S.VAL_ADDRESS
        ),
    )

    delegator_address: AccAddress
    validator_address: ValAddress

    def __post_init__(self):
        self.delegator_address = validate_acc_address(self.delegator_address)
        self.validator_address = validate_val_address(self.validator_address)

    @classmethod
    def from_data(cls, data: dict) -> MsgWithdrawDelegationReward:
        data = data["value"]
        return cls(
            delegator_address=data["delegator_address"],
            validator_address=data["validator_address"],
        )


@dataclass
class MsgWithdrawValidatorCommission(StdMsg):

    type = "distribution/MsgWithdrawValidatorCommission"
    action = "withdraw_validator_commission"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^distribution/MsgWithdrawValidatorCommission\Z"),
        value=S.OBJECT(validator_address=S.VAL_ADDRESS),
    )

    validator_address: ValAddress

    def __post_init__(self):
        self.validator_address = validate_val_address(self.validator_address)

    @classmethod
    def from_data(cls, data: dict) -> MsgWithdrawValidatorCommission:
        data = data["value"]
        return cls(validator_address=data["validator_address"])
