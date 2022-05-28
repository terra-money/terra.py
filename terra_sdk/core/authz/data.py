"""Authz module data types."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

import attr
from betterproto.lib.google.protobuf import Any as Any_pb
from dateutil import parser
from terra_proto.cosmos.authz.v1beta1 import (
    GenericAuthorization as GenericAuthorization_pb,
)
from terra_proto.cosmos.authz.v1beta1 import Grant as Grant_pb
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
    "StakeAuthorization",
    "AuthorizationGrant",
    "AuthorizationType",
]


class Authorization(BaseTerraData):
    """Base class for authorization types."""

    @staticmethod
    def from_amino(amino: dict) -> Authorization:
        from terra_sdk.util.parse_authorization import parse_authorization_amino

        return parse_authorization_amino(amino)

    @staticmethod
    def from_data(data: dict) -> Authorization:
        from terra_sdk.util.parse_authorization import parse_authorization

        return parse_authorization(data)

    @staticmethod
    def from_proto(proto: Any_pb) -> Authorization:
        from terra_sdk.util.parse_authorization import parse_authorization_proto

        return parse_authorization_proto(proto)

    @staticmethod
    def unpack_any(proto: Any_pb) -> Authorization:
        from terra_sdk.util.parse_authorization import parse_authorization_unpack_any

        return parse_authorization_unpack_any(proto)


@attr.s
class SendAuthorization(Authorization):
    """Type of :class:`Authorization` for :class:`MsgSend<terra_sdk.core.bank.msgs.MsgSend>`,
    which can be parameterized by setting a ``spend_limit`` allowance for the grantee.

    Args:
        spend_limit (Coins.Input): coins representing allowance of grant
    """

    type_amino = "cosmos-sdk/SendAuthorization"
    """"""
    type_url = "/cosmos.bank.v1beta1.SendAuthorization"
    """"""
    prototype = SendAuthorization_pb
    """"""

    spend_limit: Coins = attr.ib(converter=Coins)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {"spend_limit": self.spend_limit.to_amino()},
        }

    def to_data(self) -> dict:
        return {"@type": self.type_url, "spend_limit": self.spend_limit.to_data()}

    @classmethod
    def from_data(cls, data: dict) -> SendAuthorization:
        return cls(spend_limit=Coins.from_data(data["spend_limit"]))

    def to_proto(self) -> SendAuthorization_pb:
        return SendAuthorization_pb(spend_limit=self.spend_limit.to_proto())

    @classmethod
    def from_proto(cls, proto: SendAuthorization_pb) -> SendAuthorization:
        return cls(spend_limit=Coins.from_proto(proto.spend_limit))

    @classmethod
    def from_amino(cls, amino: dict) -> SendAuthorization:
        value = amino["value"]
        return cls(spend_limit=Coins.from_amino(value["spend_limit"]))

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))


@attr.s
class GenericAuthorization(Authorization):
    """Generic type of :class:`Authorization`, specifying the type of message to allow.

    Args:
        msg: type of message allowed by authorization"""

    type_amino = "cosmos-sdk/GenericAuthorization"
    """"""
    type_url = "/cosmos.authz.v1beta1.GenericAuthorization"
    """"""
    prototype = GenericAuthorization_pb
    """"""

    msg: str = attr.ib()

    def to_amino(self) -> dict:
        return {"type": self.type_amino, "value": {"msg": self.msg}}

    def to_data(self) -> dict:
        return {"@type": self.type_url, "msg": self.msg}

    @classmethod
    def from_data(cls, data: dict) -> GenericAuthorization:
        return cls(msg=data["msg"])

    def to_proto(self) -> GenericAuthorization_pb:
        return GenericAuthorization_pb(msg=self.msg)

    @classmethod
    def from_proto(cls, proto: GenericAuthorization_pb) -> GenericAuthorization:
        return cls(msg=proto.msg)

    @classmethod
    def from_amino(cls, amino: dict) -> GenericAuthorization:
        value = amino["value"]
        return cls(msg=value["msg"])

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))


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
            "expiration": to_isoformat(self.expiration),
        }

    def to_data(self) -> dict:
        return {
            "authorization": self.authorization.to_data(),
            "expiration": to_isoformat(self.expiration),
        }

    @classmethod
    def from_data(cls, data: dict) -> AuthorizationGrant:
        return cls(
            authorization=Authorization.from_data(data["authorization"]),
            expiration=data["expiration"],
        )

    def to_proto(self) -> Grant_pb:
        return Grant_pb(
            authorization=self.authorization.pack_any(),
            expiration=self.expiration,
        )

    @classmethod
    def from_proto(cls, proto: Grant_pb) -> AuthorizationGrant:
        return cls(
            authorization=Authorization.unpack_any(proto.authorization),
            expiration=proto.expiration,
        )

    @classmethod
    def from_amino(cls, amino: dict) -> AuthorizationGrant:
        value = amino["value"]
        return cls(
            authorization=Authorization.from_amino(value["authorization"]),
            expiration=value["expiration"],
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

    @classmethod
    def from_proto(
        cls, proto: StakeAuthorizationValidators_pb
    ) -> StakeAuthorizationValidators:
        return cls(address=proto.address)


@attr.s
class StakeAuthorization(Authorization):
    authorization_type: AuthorizationType = attr.ib()
    max_tokens: Optional[Coin] = attr.ib(default=None)
    allow_list: Optional[StakeAuthorizationValidators] = attr.ib(default=None)
    deny_list: Optional[StakeAuthorizationValidators] = attr.ib(default=None)

    type_url = "/cosmos.staking.v1beta1.StakeAuthorization"
    """"""
    prototype = StakeAuthorization_pb
    """"""

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
            max_tokens=(
                Coin.from_data(data["max_tokens"])
                if data.get("max_tokens") is not None
                else None
            ),
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

    @classmethod
    def from_proto(cls, proto: StakeAuthorization_pb) -> StakeAuthorization:
        return StakeAuthorization(
            authorization_type=proto.authorization_type,
            max_tokens=Coin.from_proto(proto.max_tokens) if proto.max_tokens else None,
            allow_list=StakeAuthorizationValidators.from_proto(proto.allow_list)
            if proto.allow_list
            else None,
            deny_list=StakeAuthorizationValidators.from_proto(proto.deny_list)
            if proto.deny_list
            else None,
        )

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))
