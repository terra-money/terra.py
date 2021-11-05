"""Authz module message types."""

from __future__ import annotations

import betterproto
from typing import List

import attr

from terra_sdk.core import AccAddress
from terra_sdk.core.msg import Msg
from terra_sdk.util.json import JSONSerializable

from terra_proto.cosmos.authz.v1beta1 import MsgExec as MsgExec_pb
from terra_proto.cosmos.authz.v1beta1 import MsgGrant as MsgGrant_pb, Grant as Grant_pb
from terra_proto.cosmos.authz.v1beta1 import MsgRevoke as MsgRevoke_pb


from .data import Authorization

__all__ = ["MsgExecAuthorized", "MsgGrantAuthorization", "MsgRevokeAuthorization"]


@attr.s
class MsgExecAuthorized(Msg):
    """Execute a set of messages, exercising an existing authorization.

    Args:
        grantee: grantee account (submitting on behalf of granter)
        msg (List[Msg]): list of messages to execute using authorization grant
    """

    type = "msgauth/MsgExecAuthorized"
    """"""
    type_url = "/cosmos.authz.v1beta1.MsgExec"
    """"""

    grantee: AccAddress = attr.ib()
    msgs: List[Msg] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgExecAuthorized:
        return cls(
            grantee=data["grantee"], msgs=[Msg.from_data(md) for md in data["msgs"]]
        )

    def to_proto(self) -> MsgExec_pb:
        return MsgExec_pb(
            grantee=self.grantee,
            msgs=[m.pack_any() for m in self.msgs]
        )


@attr.s
class Grant(JSONSerializable):
    authorization: Authorization = attr.ib()
    expiration: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> Grant:
        return cls(
            authorization=Authorization.from_data(data["authorization"]),
            expiration=data["expiration"]
        )

    def to_proto(self) -> Grant_pb:
        return Grant_pb(
            authorization=self.authorization.to_proto(),
            expiration=betterproto.datetime.fromisoformat(self.expiration)
        )


@attr.s
class MsgGrantAuthorization(Msg):
    """Grant an authorization to ``grantee`` to call messages on behalf of ``granter``.

    Args:
        granter: account granting authorization
        grantee: account receiving authorization
        grant: pair of authorization, expiration
    """

    type = "msgauth/MsgGrantAuthorization"
    """"""
    type_url = "/cosmos.authz.v1beta1.MsgGrant"
    """"""

    granter: AccAddress = attr.ib()
    grantee: AccAddress = attr.ib()
    grant: Grant = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgGrantAuthorization:
        data = data["value"]
        return cls(
            granter=data["granter"],
            grantee=data["grantee"],
            grant=Grant(
                authorization=Authorization.from_data(data["grant"]["authorization"]),
                expiration=str(data["grant"]["expiration"]),
            ),
        )

    def to_proto(self) -> MsgGrant_pb:
        return MsgGrant_pb(
            granter=self.granter,
            grantee=self.grantee,
            grant=self.grant.to_proto()
        )

@attr.s
class MsgRevokeAuthorization(Msg):
    """Remove existing authorization grant of the specified message type.

    Args:
        granter: account removing authorization
        grantee: account having authorization removed
        msg_type_url: type of message to remove authorization for
    """

    type = "msgauth/MsgRevokeAuthorization"
    """"""
    type_url = "/cosmos.authz.v1beta1.MsgRevoke"
    """"""

    granter: AccAddress = attr.ib()
    grantee: AccAddress = attr.ib()
    msg_type_url: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgRevokeAuthorization:
        return cls(
            granter=data["granter"],
            grantee=data["grantee"],
            msg_type_url=data["msg_type_url"],
        )

    def to_proto(self) -> MsgRevoke_pb:
        return MsgRevoke_pb(
            granter=self.granter,
            grantee=self.grantee,
            msg_type_url=self.msg_type_url
        )
