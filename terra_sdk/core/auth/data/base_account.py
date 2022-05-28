"""Data objects pertaining to accounts."""

from __future__ import annotations

from typing import Optional

import attr
from terra_proto.cosmos.auth.v1beta1 import BaseAccount as BaseAccount_pb

from ....core import AccAddress
from ....util.json import JSONSerializable
from ...public_key import PublicKey

__all__ = ["BaseAccount"]


@attr.s
class BaseAccount(JSONSerializable):
    """Stores information about an account."""

    type_amino = "cosmos-sdk/BaseAccount"
    type_url = "/cosmos.auth.v1beta1.BaseAccount"

    address: AccAddress = attr.ib()
    """"""

    public_key: Optional[PublicKey] = attr.ib()
    """"""

    account_number: int = attr.ib(converter=int)
    """"""

    sequence: int = attr.ib(converter=int)
    """"""

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "address": self.address,
                "public_key": self.public_key.to_amino() if self.public_key else None,
                "account_number": str(self.account_number),
                "sequence": str(self.sequence),
            },
        }

    @classmethod
    def from_amino(cls, amino: dict) -> BaseAccount:
        amino = amino["value"] if "value" in amino else amino
        return cls(
            address=amino["address"],
            public_key=PublicKey.from_amino(amino["public_key"])
            if amino["public_key"]
            else None,
            account_number=amino["account_number"],
            sequence=amino["sequence"],
        )

    def get_account_number(self) -> int:
        return self.account_number

    def get_sequence(self) -> int:
        return self.sequence

    def get_public_key(self) -> PublicKey:
        return self.public_key

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "address": self.address,
            "pub_key": self.public_key and self.public_key.to_data(),
            "account_number": str(self.account_number),
            "sequence": str(self.sequence),
        }

    @classmethod
    def from_data(cls, data: dict) -> BaseAccount:
        return cls(
            address=data["address"],
            public_key=data.get("pub_key") and PublicKey.from_data(data["pub_key"]),
            account_number=data.get("account_number") or 0,
            sequence=data.get("sequence") or 0,
        )

    @classmethod
    def from_proto(cls, proto: BaseAccount_pb) -> BaseAccount:
        return cls(
            address=proto.address,
            public_key=PublicKey.from_proto(proto.pub_key),
            account_number=proto.account_number,
            sequence=proto.sequence,
        )

    def to_proto(self) -> BaseAccount_pb:
        return BaseAccount_pb(
            address=self.address,
            pub_key=self.public_key.to_proto() if self.public_key else None,
            account_number=self.account_number,
            sequence=self.sequence,
        )
