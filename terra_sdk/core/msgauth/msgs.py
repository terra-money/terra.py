from __future__ import annotations

from terra_sdk.util.base import BaseTerraData

__all__ = [
    "MsgExecAuthorized",
    "MsgGrantAuthorization",
    "MsgRevokeAuthorization"
]


class MsgExecAuthorized(BaseTerraData):
    type = 'msgauth/MsgExecAuthorized'


class MsgGrantAuthorization(BaseTerraData):
    type = 'msgauth/MsgExecAuthorized'


class MsgRevokeAuthorization(BaseTerraData):
    type = 'msgauth/MsgRevokeAuthorization'
