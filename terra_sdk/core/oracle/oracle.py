from __future__ import annotations

import attr
from typing import Dict, Union

from terra_sdk.core import Coin, Dec, ValAddress
from terra_sdk.util.serdes import JsonDeserializable, JsonSerializable
from terra_sdk.util.validation import Schemas as S
from terra_sdk.util.validation import validate_val_address

__all__ = ["ExchangeRatePrevote", "ExchangeRateVote"]


@attr.s
class ExchangeRateVote(JsonSerializable, JsonDeserializable):


    exchange_rate: Coin= attr.ib()
    denom: str        = attr.ib()
    voter: ValAddress = attr.ib()

    def __post_init__(self):
        self.voter = validate_val_address(self.voter)

    def to_data(self) -> Dict[str, Union[Dec, str, ValAddress]]:
        return {
            "exchange_rate": str(self.exchange_rate.amount),
            "denom": self.denom,
            "voter": self.voter,
        }

    @classmethod
    def from_data(cls, data) -> ExchangeRateVote:
        xr = Coin(data["denom"], data["exchange_rate"])
        return cls(exchange_rate=xr, denom=xr.denom, voter=data["voter"])


@attr.s
class ExchangeRatePrevote(JsonSerializable, JsonDeserializable):


    hash: str         = attr.ib()
    denom: str        = attr.ib()
    voter: ValAddress = attr.ib()
    submit_block: int = attr.ib()

    def __post_init__(self):
        self.voter = validate_val_address(self.voter)
        self.submit_block = int(self.submit_block)

    def to_data(self) -> Dict[str, str]:
        return {
            "hash": self.hash,
            "denom": self.denom,
            "voter": self.voter,
            "submit_block": str(self.submit_block),
        }

    @classmethod
    def from_data(cls, data: Dict[str, str]) -> ExchangeRatePrevote:
        return cls(
            hash=data["hash"],
            denom=data["denom"],
            voter=data["voter"],
            submit_block=int(data["submit_block"]),
        )
