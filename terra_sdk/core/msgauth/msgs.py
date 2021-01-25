from __future__ import annotations

from terra_sdk.util.base import BaseTerraData

import attr

__all__ = ["MsgExecAuthorized", "MsgGrantAuthorization", "MsgRevokeAuthorization"]


@attr.s
class MsgExecAuthorized(BaseTerraData):
    type = "msgauth/MsgExecAuthorized"

    grantee: AccAddress = attr.ib()
    msgs: List[Msg] = attr.ib()


@attr.s
class MsgGrantAuthorization(BaseTerraData):
    type = "msgauth/MsgGrantAuthorization"

    granter: AccAddress = attr.ib()
    grantee: AccAddress = attr.ib()
    authorization: Authorization = attr.ib()
    period: int = attr.ib()


@attr.s
class MsgRevokeAuthorization(BaseTerraData):
    type = "msgauth/MsgRevokeAuthorization"

    granter: AccAddress = attr.ib()
    grantee: AccAddress = attr.ib()
    authorization_msg_type: str = attr.ib()
