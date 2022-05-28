from __future__ import annotations

import copy
from datetime import datetime
from typing import Union

import attr
from dateutil import parser
from terra_proto.cosmos.staking.v1beta1 import BondStatus
from terra_proto.cosmos.staking.v1beta1 import Commission as Commission_pb
from terra_proto.cosmos.staking.v1beta1 import CommissionRates as CommissionRates_pb
from terra_proto.cosmos.staking.v1beta1 import Description as Description_pb
from terra_proto.cosmos.staking.v1beta1 import Validator as Validator_pb

from terra_sdk.core import Dec, ValAddress, ValConsPubKey
from terra_sdk.util.converter import to_isoformat
from terra_sdk.util.json import JSONSerializable

__all__ = ["CommissionRates", "Commission", "Description", "Validator", "BondStatus"]


def convert_bond_status_to_json(status: BondStatus) -> str:
    if status == BondStatus.BOND_STATUS_UNSPECIFIED:
        return "BOND_STATUS_UNSPECIFIED"
    elif status == BondStatus.BOND_STATUS_UNBONDED:
        return "BOND_STATUS_UNBONDED"
    elif status == BondStatus.BOND_STATUS_UNBONDING:
        return "BOND_STATUS_UNBONDING"
    elif status == BondStatus.BOND_STATUS_BONDED:
        return "BOND_STATUS_BONDED"


def convert_bond_status_from_json(status: str) -> BondStatus:
    if status == 0 or status == "BOND_STATUS_UNSPECIFIED":
        return BondStatus.BOND_STATUS_UNSPECIFIED
    elif status == 1 or status == "BOND_STATUS_UNBONDED":
        return BondStatus.BOND_STATUS_UNBONDED
    elif status == 2 or status == "BOND_STATUS_UNBONDING":
        return BondStatus.BOND_STATUS_UNBONDING
    elif status == 3 or status == "BOND_STATUS_BONDED":
        return BondStatus.BOND_STATUS_BONDED


@attr.s
class CommissionRates(JSONSerializable):
    """Data structure for validator's commission rates & policy."""

    rate: Dec = attr.ib(converter=Dec)
    """Current % commission rate."""

    max_rate: Dec = attr.ib(converter=Dec)
    """Maximum % commission rate permitted by policy."""

    max_change_rate: Dec = attr.ib(converter=Dec)
    """Maximum % change of commission per day."""

    def to_amino(self) -> dict:
        return {
            "rate": str(self.rate),
            "max_rate": str(self.max_rate),
            "max_change_rate": str(self.max_change_rate),
        }

    def to_data(self) -> dict:
        return {
            "rate": self.rate.to_data(),
            "max_rate": self.max_rate.to_data(),
            "max_change_rate": self.max_change_rate.to_data(),
        }

    @classmethod
    def from_data(cls, data: dict) -> CommissionRates:
        return cls(
            rate=data["rate"],
            max_rate=data["max_rate"],
            max_change_rate=data["max_change_rate"],
        )

    def to_proto(self) -> CommissionRates_pb:
        return CommissionRates_pb(
            rate=str(self.rate),
            max_rate=str(self.max_rate),
            max_change_rate=str(self.max_change_rate),
        )

    @classmethod
    def from_proto(cls, proto: CommissionRates_pb) -> CommissionRates:
        return cls(
            rate=proto.rate,
            max_rate=proto.max_rate,
            max_change_rate=proto.max_change_rate,
        )


@attr.s
class Commission(JSONSerializable):
    """Contains information about validator's commission rates."""

    commission_rates: CommissionRates = attr.ib()
    """Validator commission rates."""

    update_time: datetime = attr.ib(converter=parser.parse)
    """Last time commission rates were updated."""

    def to_amino(self) -> dict:
        return {
            "commission_rates": self.commission_rates.to_amino(),
            "update_time": to_isoformat(self.update_time),
        }

    def to_amino(self) -> dict:
        return {
            "commission_rates": self.commission_rates.to_data(),
            "update_time": to_isoformat(self.update_time),
        }

    @classmethod
    def from_data(cls, data: dict) -> Commission:
        return cls(
            commission_rates=CommissionRates.from_data(data["commission_rates"]),
            update_time=data["update_time"],
        )

    def to_proto(self) -> Commission_pb:
        return Commission_pb(
            commission_rates=self.commission_rates.to_proto(),
            update_time=self.update_time,
        )


@attr.s
class Description(JSONSerializable):
    """Validator description entry.

    Args:
        moniker: validator name, aka: \"Terran One\"
        identity: keybase.io identifier (used for setting logo)
        website: validator website
        details: longer description of validator
        security_contact: contact information for validator
    """

    DO_NOT_MODIFY = "[do-not-modify]"
    """"""

    moniker: str = attr.ib(default="")
    identity: str = attr.ib(default="")
    website: str = attr.ib(default="")
    details: str = attr.ib(default="")
    security_contact: str = attr.ib(default="")

    def to_amino(self) -> dict:
        return {
            "moniker": self.moniker,
            "identity": self.identity,
            "website": self.website,
            "details": self.details,
            "security_contact": self.security_contact,
        }

    def to_data(self) -> dict:
        return {
            "moniker": self.moniker,
            "identity": self.identity,
            "website": self.website,
            "details": self.details,
            "security_contact": self.security_contact,
        }

    @classmethod
    def from_data(cls, data) -> Description:
        return cls(
            data.get("moniker"),
            data.get("identity"),
            data.get("website"),
            data.get("details"),
            data.get("security_contact"),
        )

    def to_proto(self) -> Description_pb:
        return Description_pb(
            moniker=self.moniker,
            identity=self.identity,
            website=self.website,
            details=self.details,
            security_contact=self.security_contact,
        )

    @classmethod
    def from_proto(cls, proto: Description_pb) -> Description:
        return cls(
            proto.moniker,
            proto.identity,
            proto.website,
            proto.details,
            proto.security_contact,
        )


@attr.s
class Validator(JSONSerializable):
    """Contains information about a registered validator."""

    operator_address: ValAddress = attr.ib()
    """"""

    consensus_pubkey: ValConsPubKey = attr.ib()
    """"""

    jailed: bool = attr.ib(converter=bool)
    """"""

    status: BondStatus = attr.ib(converter=BondStatus)
    """"""

    tokens: int = attr.ib(converter=int)
    """"""

    delegator_shares: Dec = attr.ib(converter=Dec)
    """"""

    description: Description = attr.ib()
    """"""

    unbonding_height: int = attr.ib(converter=int)
    """"""

    unbonding_time: datetime = attr.ib(converter=parser.parse)
    """"""

    commission: Commission = attr.ib()
    """"""

    min_self_delegation: int = attr.ib(converter=int)
    """"""

    def to_amino(self) -> dict:
        return {
            "operator_address": self.operator_address,
            "consensus_pubkey": self.consensus_pubkey,
            "jailed": self.jailed,
            "status": self.status,
            "tokens": str(self.tokens),
            "delegator_shares": str(self.delegator_shares),
            "description": self.description.to_amino(),
            "unbonding_height": str(self.unbonding_height),
            "unbonding_time": to_isoformat(self.unbonding_time),
            "commission": self.commission.to_amino(),
            "min_self_delegation": str(self.min_self_delegation),
        }

    def to_data(self) -> dict:
        return {
            "operator_address": self.operator_address,
            "consensus_pubkey": self.consensus_pubkey,
            "jailed": self.jailed,
            "status": convert_bond_status_to_json(self.status),
            "tokens": str(self.tokens),
            "delegator_shares": str(self.delegator_shares),
            "description": self.description.to_amino(),
            "unbonding_height": str(self.unbonding_height),
            "unbonding_time": to_isoformat(self.unbonding_time),
            "commission": self.commission.to_amino(),
            "min_self_delegation": str(self.min_self_delegation),
        }

    @classmethod
    def from_data(cls, data: dict) -> Validator:
        return cls(
            operator_address=data["operator_address"],
            consensus_pubkey=data["consensus_pubkey"],
            jailed=data.get("jailed"),
            status=convert_bond_status_from_json(data["status"]),
            tokens=data["tokens"],
            delegator_shares=data["delegator_shares"],
            description=Description.from_data(data["description"]),
            unbonding_height=data.get("unbonding_height") or 0,
            unbonding_time=data["unbonding_time"],
            commission=Commission.from_data(data["commission"]),
            min_self_delegation=data["min_self_delegation"],
        )

    def to_proto(self) -> Validator_pb:
        return Validator_pb(
            operator_address=self.operator_address,
            consensus_pubkey=self.consensus_pubkey.to_proto(),
            jailed=self.jailed,
            status=self.status,
            tokens=str(self.tokens),
            delegator_shares=str(self.delegator_shares),
            description=self.description.to_proto(),
            unbonding_height=self.unbonding_height,
            unbonding_time=self.unbonding_time,
            commission=self.commission.to_proto(),
            min_self_delegation=str(self.min_self_delegation),
        )
