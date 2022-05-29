"""Authz module message types."""

from __future__ import annotations

from typing import List

import attr
from betterproto.lib.google.protobuf import Any as Any_pb
from terra_proto.cosmos.authz.v1beta1 import MsgExec as MsgExec_pb
from terra_proto.cosmos.authz.v1beta1 import MsgGrant as MsgGrant_pb
from terra_proto.cosmos.authz.v1beta1 import MsgRevoke as MsgRevoke_pb

from terra_sdk.core import AccAddress
from terra_sdk.core.msg import Msg

from .data import Authorization, AuthorizationGrant

__all__ = ["MsgExecAuthorized", "MsgGrantAuthorization", "MsgRevokeAuthorization"]


@attr.s
class MsgExecAuthorized(Msg):
    """Execute a set of messages, exercising an existing authorization.

    Args:
        grantee: grantee account (submitting on behalf of granter)
        msg (List[Msg]): list of messages to execute using authorization grant
    """

    type_amino = "cosmos-sdk/MsgExecAuthorized"
    """"""
    type_url = "/cosmos.authz.v1beta1.MsgExec"
    """"""
    prototype = MsgExec_pb
    """"""

    grantee: AccAddress = attr.ib()
    msgs: List[Msg] = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "grantee": self.grantee,
                "msgs": [msg.to_amino() for msg in self.msgs],
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "grantee": self.grantee,
            "msgs": [msg.to_data() for msg in self.msgs],
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgExecAuthorized:
        return cls(
            grantee=data["grantee"], msgs=[Msg.from_data(md) for md in data["msgs"]]
        )

    def to_proto(self) -> MsgExec_pb:
        return MsgExec_pb(grantee=self.grantee, msgs=[m.pack_any() for m in self.msgs])

    @classmethod
    def from_proto(cls, proto: MsgExec_pb) -> MsgExecAuthorized:
        return cls(
            grantee=proto.grantee, msgs=[Msg.from_proto(md) for md in proto.msgs]
        )

    @classmethod
    def from_amino(cls, amino: dict) -> MsgExecAuthorized:
        value = amino["value"]
        return cls(
            grantee=value["grantee"],
            msgs=[Msg.from_amino(msg) for msg in value["msgs"]],
        )

    @classmethod
    def unpack_any(cls, any_pb: Any_pb) -> MsgExecAuthorized:
        return cls.from_proto(MsgExec_pb().parse(any_pb.value))


@attr.s
class MsgGrantAuthorization(Msg):
    """Grant an authorization to ``grantee`` to call messages on behalf of ``granter``.

    Args:
        granter: account granting authorization
        grantee: account receiving authorization
        grant: pair of authorization, expiration
    """

    type_amino = "cosmos-sdk/MsgGrantAuthorization"
    """"""
    type_url = "/cosmos.authz.v1beta1.MsgGrant"
    """"""
    prototype = MsgGrant_pb
    """"""

    granter: AccAddress = attr.ib()
    grantee: AccAddress = attr.ib()
    grant: AuthorizationGrant = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "granter": self.granter,
                "grantee": self.grantee,
                "grant": self.grant.to_amino(),
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "granter": self.granter,
            "grantee": self.grantee,
            "grant": self.grant.to_data(),
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgGrantAuthorization:
        return cls(
            granter=data["granter"],
            grantee=data["grantee"],
            grant=AuthorizationGrant.from_data(data["grant"]),
        )

    def to_proto(self) -> MsgGrant_pb:
        return MsgGrant_pb(
            granter=self.granter, grantee=self.grantee, grant=self.grant.to_proto()
        )

    @classmethod
    def from_proto(cls, proto: MsgGrant_pb) -> MsgGrantAuthorization:
        return cls(
            granter=proto.granter,
            grantee=proto.grantee,
            grant=AuthorizationGrant.from_proto(proto.grant),
        )

    @classmethod
    def from_amino(cls, amino: dict) -> MsgGrantAuthorization:
        value = amino["value"]
        return cls(
            grantee=value["grantee"],
            granter=value["granter"],
            grant=AuthorizationGrant.from_amino(value["grant"]),
        )


@attr.s
class MsgRevokeAuthorization(Msg):
    """Remove existing authorization grant of the specified message type.

    Args:
        granter: account removing authorization
        grantee: account having authorization removed
        msg_type_url: type of message to remove authorization for
    """

    type_amino = "cosmos-sdk/MsgRevokeAuthorization"
    """"""
    type_url = "/cosmos.authz.v1beta1.MsgRevoke"
    """"""
    prototype = MsgRevoke_pb
    """"""

    granter: AccAddress = attr.ib()
    grantee: AccAddress = attr.ib()
    msg_type_url: str = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "granter": self.granter,
                "grantee": self.grantee,
                "msg_type_url": self.msg_type_url,
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "granter": self.granter,
            "grantee": self.grantee,
            "msg_type_url": self.msg_type_url,
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgRevokeAuthorization:
        return cls(
            granter=data["granter"],
            grantee=data["grantee"],
            msg_type_url=data["msg_type_url"],
        )

    def to_proto(self) -> MsgRevoke_pb:
        return MsgRevoke_pb(
            granter=self.granter, grantee=self.grantee, msg_type_url=self.msg_type_url
        )

    @classmethod
    def from_proto(cls, proto: MsgRevoke_pb) -> MsgRevokeAuthorization:
        return cls(
            granter=proto.granter,
            grantee=proto.grantee,
            msg_type_url=proto.msg_type_url,
        )
