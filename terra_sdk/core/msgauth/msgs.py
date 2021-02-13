"""MsgAuth module message types."""

from __future__ import annotations

import copy
from typing import List

import attr

from terra_sdk.core import AccAddress
from terra_sdk.core.msg import Msg
from terra_sdk.util.json import dict_to_data

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
class MsgGrantAuthorization(Msg):
    """Grant an authorization to ``grantee`` to call messages on behalf of ``granter``.

    Args:
        granter: account giving authorization
        grantee: account receiving authorization
        authorization: details of authorization granted
        period (int): timeframe during which the authorization is considered valid
    """

    type = "msgauth/MsgGrantAuthorization"

    granter: AccAddress = attr.ib()
    grantee: AccAddress = attr.ib()
    authorization: Authorization = attr.ib()
    period: int = attr.ib(converter=int)

    def to_data(self) -> dict:
        d = copy.deepcopy(self.__dict__)
        d["period"] = str(d["period"])
        return {"type": self.type, "value": dict_to_data(d)}

    @classmethod
    def from_data(cls, data: dict) -> MsgGrantAuthorization:
        data = data["value"]
        return cls(
            granter=data["granter"],
            grantee=data["grantee"],
            authorization=Authorization.from_data(data["authorization"]),
            period=data["period"],
        )


@attr.s
class MsgRevokeAuthorization(Msg):
    """Remove existing authorization grant of the specified message type.

    Args:
        granter: account removing authorization
        grantee: account having authorization removed
        authorization_msg_type: type of message to remove authorization for
    """

    type = "msgauth/MsgRevokeAuthorization"
    """"""

    granter: AccAddress = attr.ib()
    grantee: AccAddress = attr.ib()
    authorization_msg_type: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgRevokeAuthorization:
        data = data["value"]
        return cls(
            granter=data["granter"],
            grantee=data["grantee"],
            authorization_msg_type=data["authorization_msg_type"],
        )
