from __future__ import annotations

import attr

from terra_sdk.core import Coins

__all__ = ["Account"]


@attr.s
class Account:
    """Stores information about an account fetched from the blockchain."""

    address: str = attr.ib()
    coins: Coins = attr.ib(converter=Coins)
    public_key: PublicKey = attr.ib()
    account_number: int = attr.ib(converter=int)
    sequence: int = attr.ib(converter=int)

    def to_data(self) -> dict:
        return {
            "type": "core/Account",
            "value": {
                "address": self.address,
                "coins": self.coins.to_data(),
                "public_key": self.public_key.to_data(),
                "account_number": str(self.account_number),
                "sequence": str(self.sequence),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> Account:
        data = data["value"]
        return cls(
            address=data["address"],
            coins=Coins.from_data(data["coins"]),
            public_key=PublicKey.from_data(data["public_key"]),
            account_number=data["account_number"],
            sequence=data["sequence"],
        )
