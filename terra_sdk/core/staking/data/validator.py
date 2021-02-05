from __future__ import annotations

import copy

import attr

from terra_sdk.core import Dec, ValAddress, ValConsPubKey
from terra_sdk.util.json import JSONSerializable, dict_to_data

__all__ = [
    "CommissionRates",
    "Commission",
    "Description",
    "Validator",
]


@attr.s
class CommissionRates(JSONSerializable):

    rate: Dec = attr.ib(converter=Dec)
    max_rate: Dec = attr.ib(converter=Dec)
    max_change_rate: Dec = attr.ib(converter=Dec)

    @classmethod
    def from_data(cls, data: dict) -> CommissionRates:
        return cls(
            rate=data["rate"],
            max_rate=data["max_rate"],
            max_change_rate=data["max_change_rate"],
        )


@attr.s
class Commission(JSONSerializable):

    commission_rates: CommissionRates = attr.ib()
    update_time: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> Commission:
        return cls(
            commission_rates=CommissionRates.from_data(data["commission_rates"]),
            update_time=data["update_time"],
        )


# from cosmos


@attr.s
class Description(JSONSerializable):

    DO_NOT_MODIFY = "[do-not-modify]"

    moniker: str = attr.ib()
    identity: str = attr.ib()
    website: str = attr.ib()
    details: str = attr.ib()

    @classmethod
    def from_data(cls, data) -> Description:
        return cls(data["moniker"], data["identity"], data["website"], data["details"])


@attr.s
class Validator(JSONSerializable):

    operator_address: ValAddress = attr.ib()
    consensus_pubkey: ValConsPubKey = attr.ib()
    jailed: bool = attr.ib()
    status: int = attr.ib(converter=int)
    tokens: int = attr.ib(converter=int)
    delegator_shares: Dec = attr.ib(converter=Dec)
    description: Description = attr.ib()
    unbonding_height: int = attr.ib(converter=int)
    unbonding_time: str = attr.ib()
    commission: Commission = attr.ib()
    min_self_delegation: int = attr.ib(converter=int)

    def to_data(self) -> dict:
        d = copy.deepcopy(self.__dict__)
        d["min_self_delegation"] = str(d["min_self_delegation"])
        d["tokens"] = str(d["tokens"])
        d["unbonding_height"] = str(d["unbonding_height"])
        return dict_to_data(d)

    @classmethod
    def from_data(cls, data: dict) -> Validator:
        return cls(
            operator_address=data["operator_address"],
            consensus_pubkey=data["consensus_pubkey"],
            jailed=data["jailed"],
            status=data["status"],
            tokens=data["tokens"],
            delegator_shares=data["delegator_shares"],
            description=Description.from_data(data["description"]),
            unbonding_height=data["unbonding_height"],
            unbonding_time=data["unbonding_time"],
            commission=Commission.from_data(data["commission"]),
            min_self_delegation=data["min_self_delegation"],
        )
