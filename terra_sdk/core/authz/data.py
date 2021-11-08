"""Authz module data types."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

import attr
from dateutil import parser
from terra_proto.cosmos.authz.v1beta1 import (
    GenericAuthorization as GenericAuthorization_pb,
)
from terra_proto.cosmos.authz.v1beta1 import Grant as Grant_pb
from terra_proto.cosmos.authz.v1beta1 import GrantAuthorization as GrantAuthorization_pb
from terra_proto.cosmos.bank.v1beta1 import SendAuthorization as SendAuthorization_pb
from terra_proto.cosmos.staking.v1beta1 import AuthorizationType
from terra_proto.cosmos.staking.v1beta1 import (
    StakeAuthorization as StakeAuthorization_pb,
)
from terra_proto.cosmos.staking.v1beta1 import (
    StakeAuthorizationValidators as StakeAuthorizationValidators_pb,
)

from terra_sdk.core import AccAddress, Coin, Coins
from terra_sdk.util.base import BaseTerraData
from terra_sdk.util.converter import to_isoformat
from terra_sdk.util.json import JSONSerializable

__all__ = [
    "Authorization",
    "SendAuthorization",
    "GenericAuthorization",
    "AuthorizationGrant",
    "AuthorizationType",
]


class Authorization(BaseTerraData):
    """Base class for authorization types."""

    @staticmethod
    def from_data(data: dict) -> Authorization:
        from terra_sdk.util.parse_authorization import parse_authorization

        return parse_authorization(data)


@attr.s
class SendAuthorization(Authorization):
    """Type of :class:`Authorization` for :class:`MsgSend<terra_sdk.core.bank.msgs.MsgSend>`,
    which can be parameterized by setting a ``spend_limit`` allowance for the grantee.

    Args:
        spend_limit (Coins.Input): coins representing allowance of grant
    """

    type_amino = "msgauth/SendAuthorization"
    """"""
    type_url = "/cosmos.bank.v1beta1.SendAuthorization"

    spend_limit: Coins = attr.ib(converter=Coins)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "spend_limit": self.spend_limit.to_amino()
            }
        }

    def to_data(self) -> dict:
        return {"@type": self.type_url, "spend_limit": self.spend_limit.to_data()}

    @classmethod
    def from_data(cls, data: dict) -> SendAuthorization:
        return cls(spend_limit=Coins.from_data(data["spend_limit"]))

    def to_proto(self) -> SendAuthorization_pb:
        return SendAuthorization_pb(spend_limit=self.spend_limit.to_proto())


@attr.s
class GenericAuthorization(Authorization):
    """Generic type of :class:`Authorization`, specifying the type of message to allow.

    Args:
        grant_msg_type: type of message allowed by authorization"""

    type_amino = "msgauth/GenericAuthorization"
    """"""
    type_url = "/cosmos.authz.v1beta1.GenericAuthorization"

    msg: str = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "msg": self.msg()
            }
        }

    def to_data(self) -> dict:
        return {"@type": self.type_url, "msg": self.msg}

    @classmethod
    def from_data(cls, data: dict) -> GenericAuthorization:
        return cls(msg=data["msg"])

    def to_proto(self) -> GenericAuthorization_pb:
        return GenericAuthorization_pb(msg=self.msg)


@attr.s
class AuthorizationGrant(JSONSerializable):
    """Contains information about an existing granted authorization between two users."""

    authorization: Authorization = attr.ib()
    """Grant authorization details."""

    expiration: datetime = attr.ib(converter=parser.parse)
    """Grant expiration."""

    def to_amino(self) -> dict:
        return {
            "authorization": self.authorization.to_amino(),
            "expiration": to_isoformat(self.expiration)
        }

    def to_data(self) -> dict:
        return {
            "authorization": self.authorization.to_data(),
            "expiration": to_isoformat(self.expiration)
        }

    @classmethod
    def from_data(cls, data: dict) -> AuthorizationGrant:
        return cls(
            authorization=Authorization.from_data(data["authorization"]),
            expiration=parser.parse(data["expiration"])
        )

    def to_proto(self) -> Grant_pb:
        return Grant_pb(
            authorization=self.authorization.to_proto(),
            expiration=self.expiration,
        )


@attr.s
class StakeAuthorizationValidators(JSONSerializable):
    address: List[AccAddress] = attr.ib(converter=list)

    def to_amino(self):
        raise Exception("Amino not supported")

    def to_data(self) -> dict:
        return {"address": self.address}

    @classmethod
    def from_data(cls, data: dict) -> StakeAuthorizationValidators:
        return cls(address=data["address"])

    def to_proto(self):
        return StakeAuthorizationValidators_pb(address=self.address)


@attr.s
class StakeAuthorization(Authorization):
    authorization_type: AuthorizationType = attr.ib()
    max_tokens: Optional[Coin] = attr.ib(converter=Coin.parse, default=None)
    allow_list: Optional[StakeAuthorizationValidators] = attr.ib(default=None)
    deny_list: Optional[StakeAuthorizationValidators] = attr.ib(default=None)

    type_url = "/cosmos.staking.v1beta1.StakeAuthorization"

    def to_amino(self):
        raise Exception("Amino not supported")

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "authorization_type": self.authorization_type,
            "max_tokens": self.max_tokens.to_data() if self.max_tokens else None,
            "allow_list": self.allow_list.to_data() if self.allow_list else None,
            "deny_list": self.deny_list.to_data() if self.deny_list else None,
        }

    @classmethod
    def from_data(cls, data: dict) -> StakeAuthorization:
        return StakeAuthorization(
            authorization_type=data["authorization_type"],
            max_tokens=Coins.from_data(data["max_tokens"])
            if data.get("max_tokens")
            else None,
            allow_list=StakeAuthorizationValidators.from_data(data["allow_list"])
            if data.get("allow_list")
            else None,
            deny_list=StakeAuthorizationValidators.from_data(data["deny_list"])
            if data.get("deny_list")
            else None,
        )

    def to_proto(self) -> StakeAuthorization_pb:
        return StakeAuthorization_pb(
            authorization_type=self.authorization_type,
            max_tokens=self.max_tokens.to_proto() if self.max_tokens else None,
            allow_list=self.allow_list.to_proto() if self.allow_list else None,
            deny_list=self.deny_list.to_proto() if self.deny_list else None,
        )
