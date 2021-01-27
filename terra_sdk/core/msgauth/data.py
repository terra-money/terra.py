from __future__ import annotations

import attrs
from terra_sdk.util.json import JSONSerializable


class Authorization(BaseTerraData):
    pass


class SendAuthorization(Authorization):
    type = "msgauth/SendAuthorization"


class GenericAuthorization(Authorization):
    type = "msgauth/SendAuthorization"


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