from __future__ import annotations

from terra_sdk.core.msg import Msg
import attr

__all__ = ["MsgExecAuthorized", "MsgGrantAuthorization", "MsgRevokeAuthorization"]


@attr.s
class MsgExecAuthorized(Msg):
    type = "msgauth/MsgExecAuthorized"

    grantee: AccAddress = attr.ib()
    msgs: List[Msg] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgExecAuthorized:
        data = data["value"]
        return cls(grantee=data["grantee"], msgs=[parse_msg(md) for md in data["msgs"]])


@attr.s
class MsgGrantAuthorization(Msg):
    type = "msgauth/MsgGrantAuthorization"

    granter: AccAddress = attr.ib()
    grantee: AccAddress = attr.ib()
    authorization: Authorization = attr.ib()
    period: int = attr.ib(conveter=int)

    @classmethod
    def from_data(cls, data: dict) -> MsgExecAuthorized:
        data = data["value"]
        return cls(
            granter=data["granter"],
            grantee=data["grantee"],
            authorization=Authorization.from_data(data["authorization"]),
            period=data["period"],
        )


@attr.s
class MsgRevokeAuthorization(Msg):
    type = "msgauth/MsgRevokeAuthorization"

    granter: AccAddress = attr.ib()
    grantee: AccAddress = attr.ib()
    authorization_msg_type: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgExecAuthorized:
        data = data["value"]
        return cls(
            granter=data["granter"],
            grantee=data["grantee"],
            authorization_msg_type=data["authorization_msg_type"],
        )