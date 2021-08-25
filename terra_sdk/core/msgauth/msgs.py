"""MsgAuth module message types."""

from __future__ import annotations

from typing import List

import attr

from terra_sdk.core import AccAddress
from terra_sdk.core.msg import Msg

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

    grantee: AccAddress = attr.ib()
    msgs: List[Msg] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgExecAuthorized:
        data = data["value"]
        return cls(
            grantee=data["grantee"], msgs=[Msg.from_data(md) for md in data["msgs"]]
        )


@attr.s
class Grant:
    granter: AccAddress = attr.ib()
    grantee: AccAddress = attr.ib()


@attr.s
class MsgGrantAuthorization(Msg):
    """Grant an authorization to ``grantee`` to call messages on behalf of ``granter``.

    Args:
        grant: pair of `granter`, `grantee`
        authorization: details of authorization granted
        expiration: time of expiry
    """

    type = "msgauth/MsgGrantAuthorization"

    grant: Grant = attr.ib()
    authorization: Authorization = attr.ib()
    expiration: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgGrantAuthorization:
        data = data["value"]
        return cls(
            grant=Grant(
                granter=data["granter"],
                grantee=data["grantee"],
            ),
            authorization=Authorization.from_data(data["authorization"]),
            expiration=str(data["expiration"]),
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

    granter: AccAddress = attr.ib()
    grantee: AccAddress = attr.ib()
    msg_type_url: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgRevokeAuthorization:
        data = data["value"]
        return cls(
            granter=data["granter"],
            grantee=data["grantee"],
            msg_type_url=data["msg_type_url"],
        )
