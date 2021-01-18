from __future__ import annotations

import hashlib

import attr

from terra_sdk.util.base import BaseMsg


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


@attr.s
class MsgExchangeRatePrevote(BaseMsg):

    type = "oracle/MsgExchangeRatePrevote"
    action = "exchangerateprevote"

    hash: str = attr.ib()
    denom: str = attr.ib()
    feeder: AccAddress = attr.ib()
    validator: ValAddress = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgExchangeRatePrevote:
        data = data["value"]
        return cls(
            hash=data["hash"],
            denom=data["denom"],
            feeder=data["feeder"],
            validator=data["validator"],
        )


@attr.s
class MsgExchangeRateVote(BaseMsg):

    type = "oracle/MsgExchangeRateVote"
    action = "exchangeratevote"

    exchange_rate: Dec = attr.ib()
    salt: str = attr.ib()
    denom: str = attr.ib()
    feeder: AccAddress = attr.ib()
    validator: ValAddress = attr.ib()

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


@attr.s
class MsgDelegateFeedConsent(BaseMsg):

    type = "oracle/MsgDelegateFeedConsent"
    action = "delegatefeeder"

    operator: ValAddress = attr.ib()
    delegate: AccAddress = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgDelegateFeedConsent:
        data = data["value"]
        return cls(operator=data["operator"], delegate=data["delegate"])
