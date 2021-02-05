from __future__ import annotations

import attr

from terra_sdk.core import Coins
from terra_sdk.util.base import BaseTerraData
from terra_sdk.util.json import JSONSerializable

__all__ = [
    "Authorization",
    "SendAuthorization",
    "GenericAuthorization",
    "AuthorizationGrant",
]


class Authorization(BaseTerraData):
    @staticmethod
    def from_data(data: dict) -> Authorization:
        from terra_sdk.util.parse_authorization import parse_authorization

        return parse_authorization(data)


@attr.s
class SendAuthorization(Authorization):
    type = "msgauth/SendAuthorization"

    spend_limit: Coins = attr.ib(converter=Coins)

    @classmethod
    def from_data(cls, data: dict) -> SendAuthorization:
        data = data["value"]
        return cls(spend_limit=Coins.from_data(data["spend_limit"]))


@attr.s
class GenericAuthorization(Authorization):
    type = "msgauth/GenericAuthorization"

    grant_msg_type: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> GenericAuthorization:
        data = data["value"]
        return cls(grant_msg_type=data["grant_msg_type"])


@attr.s
class AuthorizationGrant(JSONSerializable):

    authorization: Authorization = attr.ib()
    expiration: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> AuthorizationGrant:
        return cls(
            authorization=Authorization.from_data(data["authorization"]),
            expiration=data["expiration"],
        )
