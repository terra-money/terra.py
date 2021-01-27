from __future__ import annotations

from terra_sdk.core.msg import Msg
import attr

__all__ = ["MsgExecAuthorized", "MsgGrantAuthorization", "MsgRevokeAuthorization"]


@attr.s
class MsgExecAuthorized(Msg):
    type = "msgauth/MsgExecAuthorized"

    grantee: AccAddress = attr.ib()
    msgs: List[Msg] = attr.ib()


@attr.s
class MsgGrantAuthorization(Msg):
    type = "msgauth/MsgGrantAuthorization"

    granter: AccAddress = attr.ib()
    grantee: AccAddress = attr.ib()
    authorization: Authorization = attr.ib()
    period: int = attr.ib()


@attr.s
class MsgRevokeAuthorization(Msg):
    type = "msgauth/MsgRevokeAuthorization"

    granter: AccAddress = attr.ib()
    grantee: AccAddress = attr.ib()
    authorization_msg_type: str = attr.ib()
