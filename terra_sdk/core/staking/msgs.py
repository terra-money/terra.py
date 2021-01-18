from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from terra_sdk.core import AccAddress, Coin, Dec, ValAddress, ValConsPubKey
from terra_sdk.core.msg import StdMsg
from terra_sdk.core.staking import CommissionRates, Description
from terra_sdk.util.validation import (
    Schemas as S,
    validate_acc_address,
    validate_val_address,
    validate_val_conspubkey,
)


@dataclass
class MsgBeginRedelegate(StdMsg):

    type = "staking/MsgBeginRedelegate"
    action = "begin_redelegate"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^staking/MsgBeginRedelegate\Z"),
        value=S.OBJECT(
            delegator_address=S.ACC_ADDRESS,
            validator_src_address=S.VAL_ADDRESS,
            validator_dst_address=S.VAL_ADDRESS,
            amount=Coin.__schema__,
        ),
    )

    delegator_address: AccAddress
    validator_src_address: ValAddress
    validator_dst_address: ValAddress
    amount: Coin

    def __post_init__(self):
        self.delegator_address = validate_acc_address(self.delegator_address)
        self.validator_src_address = validate_val_address(self.validator_src_address)
        self.validator_dst_address = validate_val_address(self.validator_dst_address)

    @classmethod
    def from_data(cls, data: dict) -> MsgBeginRedelegate:
        data = data["value"]
        return cls(
            delegator_address=data["delegator_address"],
            validator_src_address=data["validator_src_address"],
            validator_dst_address=data["validator_dst_address"],
            amount=Coin.from_data(data["amount"]),
        )


@dataclass
class MsgDelegate(StdMsg):

    type = "staking/MsgDelegate"
    action = "delegate"

    schema = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^staking/MsgDelegate\Z"),
        value=S.OBJECT(
            delegator_address=S.ACC_ADDRESS,
            validator_address=S.VAL_ADDRESS,
            amount=Coin.__schema__,
        ),
    )

    delegator_address: AccAddress
    validator_address: ValAddress
    amount: Coin

    def __post_init__(self):
        self.delegator_address = validate_acc_address(self.delegator_address)
        self.validator_address = validate_val_address(self.validator_address)

    @classmethod
    def from_data(cls, data: dict) -> MsgDelegate:
        data = data["value"]
        return cls(
            delegator_address=data["delegator_address"],
            validator_address=data["validator_address"],
            amount=Coin.from_data(data["amount"]),
        )


@dataclass
class MsgUndelegate(StdMsg):

    type = "staking/MsgUndelegate"
    action = "begin_unbonding"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^staking/MsgUndelegate\Z"),
        value=S.OBJECT(
            delegator_address=S.ACC_ADDRESS,
            validator_address=S.VAL_ADDRESS,
            amount=Coin.__schema__,
        ),
    )

    delegator_address: AccAddress
    validator_address: ValAddress
    amount: Coin

    def __post_init__(self):
        self.delegator_address = validate_acc_address(self.delegator_address)
        self.validator_address = validate_val_address(self.validator_address)

    @classmethod
    def from_data(cls, data: dict) -> MsgUndelegate:
        data = data["value"]
        return cls(
            delegator_address=data["delegator_address"],
            validator_address=data["validator_address"],
            amount=Coin.from_data(data["amount"]),
        )


@dataclass
class MsgEditValidator(StdMsg):

    type = "staking/MsgEditValidator"
    action = "edit_validator"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^staking/MsgEditValidator\Z"),
        value=S.OBJECT(
            Description=Description.__schema__,
            address=S.VAL_ADDRESS,
            commission_rate=S.OPTIONAL(Dec.__schema__),
            min_self_delegation=S.OPTIONAL(S.STRING_INTEGER),
        ),
    )

    Description: Description
    address: ValAddress
    commission_rate: Optional[Dec] = None
    min_self_delegation: Optional[int] = None

    def __post_init__(self):
        if self.commission_rate is not None:
            self.commission_rate = Dec(self.commission_rate)
        if self.min_self_delegation is not None:
            self.min_self_delegation = int(self.min_self_delegation)
        self.address = validate_val_address(self.address)

    def msg_value(self) -> dict:
        d = dict(self.__dict__)
        msd = self.min_self_delegation
        if msd is not None:
            msd = str(msd)
        d["min_self_delegation"] = msd
        return d

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


@dataclass
class MsgCreateValidator(StdMsg):

    type = "staking/MsgCreateValidator"
    action = "create_validator"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^staking/MsgCreateValidator\Z"),
        value=S.OBJECT(
            description=Description.__schema__,
            commission=CommissionRates.__schema__,
            min_self_delegation=S.STRING_INTEGER,
            delegator_address=S.ACC_ADDRESS,
            validator_address=S.VAL_ADDRESS,
            pubkey=S.VAL_CONSPUBKEY,
            value=Coin.__schema__,
        ),
    )

    description: Description
    commission: CommissionRates
    min_self_delegation: int
    delegator_address: AccAddress
    validator_address: ValAddress
    pubkey: ValConsPubKey
    value: Coin

    def __post_init__(self):
        self.delegator_address = validate_acc_address(self.delegator_address)
        self.validator_address = validate_val_address(self.validator_address)
        validate_val_conspubkey(self.pubkey)
        self.min_self_delegation = int(self.min_self_delegation)

    def msg_value(self) -> dict:
        d = dict(self.__dict__)
        msd = self.min_self_delegation
        d["min_self_delegation"] = str(msd)
        return d

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
