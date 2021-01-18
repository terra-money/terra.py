from __future__ import annotations

import hashlib
from dataclasses import dataclass
from decimal import Decimal
from typing import Type, Union

from terra_sdk.core import AccAddress, Coin, Dec, ValAddress
from terra_sdk.core.msg import StdMsg
from terra_sdk.util.validation import Schemas as S
from terra_sdk.util.validation import (
    validate_acc_address,
    validate_same_denom,
    validate_val_address,
)

__all__ = [
    "vote_hash",
    "MsgExchangeRatePrevote",
    "MsgExchangeRateVote",
    "MsgDelegateFeedConsent",
]


def vote_hash(salt: str, exchange_rate: Dec, denom: str, validator: str) -> str:
    payload = f"{salt}:{exchange_rate}:{denom}:{validator}"
    sha_hash = hashlib.sha256(payload.encode())
    return sha_hash.hexdigest()[:40]


@dataclass
class MsgExchangeRatePrevote(StdMsg):

    type = "oracle/MsgExchangeRatePrevote"
    action = "exchangerateprevote"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^oracle/MsgExchangeRatePrevote\Z"),
        value=S.OBJECT(
            hash=S.STRING,
            denom=S.STRING,
            feeder=S.ACC_ADDRESS,
            validator=S.VAL_ADDRESS,
        ),
    )

    hash: str
    denom: str
    feeder: AccAddress
    validator: ValAddress

    def __post_init__(self):
        self.feeder = AccAddress(self.feeder)
        self.validator = ValAddress(self.validator)

    @classmethod
    def from_data(cls, data: dict) -> MsgExchangeRatePrevote:
        data = data["value"]
        return cls(
            hash=data["hash"],
            denom=data["denom"],
            feeder=data["feeder"],
            validator=data["validator"],
        )


@dataclass
class MsgExchangeRateVote(StdMsg):

    type = "oracle/MsgExchangeRateVote"
    action = "exchangeratevote"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^oracle/MsgExchangeRateVote\Z"),
        value=S.OBJECT(
            exchange_rate=Dec.__schema__,
            salt=S.STRING,
            denom=S.STRING,
            feeder=S.ACC_ADDRESS,
            validator=S.VAL_ADDRESS,
        ),
    )

    exchange_rate: Union[str, Type[Decimal], Coin, int]
    salt: str
    denom: str
    feeder: AccAddress
    validator: ValAddress

    def __post_init__(self):
        self.feeder = validate_acc_address(self.feeder)
        self.validator = validate_val_address(self.validator)
        if not isinstance(self.exchange_rate, Coin):
            self.exchange_rate = Coin(self.denom, self.exchange_rate)
        else:
            validate_same_denom(self.exchange_rate.denom, self.denom)

    def msg_value(self) -> dict:
        d = dict(self.__dict__)
        d["exchange_rate"] = str(self.exchange_rate.amount)
        return d

    @property
    def vote_hash(self):
        return vote_hash(
            self.salt, self.exchange_rate.amount, self.denom, self.validator
        )

    @property
    def prevote(self):
        return MsgExchangeRatePrevote(
            hash=self.vote_hash,
            denom=self.denom,
            feeder=self.feeder,
            validator=self.validator,
        )

    @classmethod
    def from_data(cls, data: dict) -> MsgExchangeRateVote:
        data = data["value"]
        xr = Coin(data["denom"], data["exchange_rate"])
        return cls(
            exchange_rate=xr,
            salt=data["salt"],
            denom=xr.denom,
            feeder=data["feeder"],
            validator=data["validator"],
        )


@dataclass
class MsgDelegateFeedConsent(StdMsg):

    type = "oracle/MsgDelegateFeedConsent"
    action = "delegatefeeder"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^oracle/MsgDelegateFeedConsent\Z"),
        value=S.OBJECT(operator=S.VAL_ADDRESS, delegate=S.ACC_ADDRESS),
    )

    operator: ValAddress
    delegate: AccAddress

    def __post_init__(self):
        self.operator = validate_val_address(self.operator)
        self.delegate = validate_acc_address(self.delegate)

    @classmethod
    def from_data(cls, data: dict) -> MsgDelegateFeedConsent:
        data = data["value"]
        return cls(operator=data["operator"], delegate=data["delegate"])
