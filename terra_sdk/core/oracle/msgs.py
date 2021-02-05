from __future__ import annotations

import copy
import hashlib

import attr

from terra_sdk.core import AccAddress, Coins, Dec, ValAddress
from terra_sdk.core.msg import Msg
from terra_sdk.util.json import dict_to_data

__all__ = [
    "vote_hash",
    "aggregate_vote_hash",
    "MsgExchangeRatePrevote",
    "MsgExchangeRateVote",
    "MsgDelegateFeedConsent",
    "MsgAggregateExchangeRatePrevote",
    "MsgAggregateExchangeRateVote",
]


def vote_hash(denom: str, exchange_rate: Dec, salt: str, validator: str) -> str:
    payload = f"{denom}:{exchange_rate!s}:{salt}:{validator}"
    sha_hash = hashlib.sha256(payload.encode())
    return sha_hash.hexdigest()[:40]


def aggregate_vote_hash(salt: str, exchange_rates: Coins, validator: str) -> str:
    payload = f"{salt}:{exchange_rates!s}:{validator}"
    sha_hash = hashlib.sha256(payload.encode())
    return sha_hash.hexdigest()[:40]


@attr.s
class MsgExchangeRatePrevote(Msg):

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
class MsgExchangeRateVote(Msg):

    type = "oracle/MsgExchangeRateVote"
    action = "exchangeratevote"

    exchange_rate: Dec = attr.ib(converter=Dec)
    salt: str = attr.ib()
    denom: str = attr.ib()
    feeder: AccAddress = attr.ib()
    validator: ValAddress = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgExchangeRateVote:
        data = data["value"]
        return cls(
            exchange_rate=data["exchange_rate"],
            salt=data["salt"],
            denom=data["denom"],
            feeder=data["feeder"],
            validator=data["validator"],
        )

    def get_vote_hash(self) -> str:
        return vote_hash(self.denom, self.exchange_rate, self.salt, self.validator)

    def get_prevote(self) -> MsgExchangeRatePrevote:
        return MsgExchangeRatePrevote(
            hash=self.get_vote_hash(),
            denom=self.denom,
            feeder=self.feeder,
            validator=self.validator,
        )


@attr.s
class MsgDelegateFeedConsent(Msg):

    type = "oracle/MsgDelegateFeedConsent"
    action = "delegatefeeder"

    operator: ValAddress = attr.ib()
    delegate: AccAddress = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgDelegateFeedConsent:
        data = data["value"]
        return cls(operator=data["operator"], delegate=data["delegate"])


@attr.s
class MsgAggregateExchangeRatePrevote(Msg):

    type = "oracle/MsgAggregateExchangeRatePrevote"

    hash: str = attr.ib()
    feeder: AccAddress = attr.ib()
    validator: ValAddress = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgAggregateExchangeRatePrevote:
        data = data["value"]
        return cls(
            hash=data["hash"],
            feeder=data["feeder"],
            validator=data["validator"],
        )


@attr.s
class MsgAggregateExchangeRateVote(Msg):

    type = "oracle/MsgAggregateExchangeRateVote"

    exchange_rates: Coins = attr.ib(converter=Coins)
    salt: str = attr.ib()
    feeder: AccAddress = attr.ib()
    validator: ValAddress = attr.ib()

    def to_data(self) -> dict:
        d = copy.deepcopy(self.__dict__)
        d["exchange_rates"] = str(self.exchange_rates)
        return {"type": self.type, "value": dict_to_data(d)}

    @classmethod
    def from_data(cls, data: dict) -> MsgAggregateExchangeRateVote:
        data = data["value"]
        return cls(
            exchange_rates=Coins.from_str(data["exchange_rates"]),
            salt=data["salt"],
            feeder=data["feeder"],
            validator=data["validator"],
        )

    def get_aggregate_vote_hash(self) -> str:
        return aggregate_vote_hash(self.salt, self.exchange_rates, self.validator)

    def get_aggregate_prevote(self) -> MsgAggregateExchangeRatePrevote:
        return MsgAggregateExchangeRatePrevote(
            hash=self.get_aggregate_vote_hash(),
            feeder=self.feeder,
            validator=self.validator,
        )
