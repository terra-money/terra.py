from __future__ import annotations

from terra_sdk.core import AccAddress, Coins
from terra_sdk.util.serdes import JsonDeserializable, JsonSerializable
from terra_sdk.util.validation import Schemas as S
from terra_sdk.util.validation import validate_acc_address

__all__ = ["Input", "Output"]


class MultiSendIO(JsonSerializable, JsonDeserializable):

    __schema__ = S.OBJECT(address=S.ACC_ADDRESS, coins=Coins.__schema__)

    def __init__(self, address: AccAddress, coins: Coins):
        address = validate_acc_address(address)
        self.address = address
        self.coins = Coins(coins)

    @classmethod
    def from_data(cls, data: dict) -> MultiSendIO:
        return cls(address=data["address"], coins=Coins.from_data(data["coins"]))


class Input(MultiSendIO):
    def __repr__(self) -> str:
        return f"Input(address='{self.address}', coins={self.coins!r})"


class Output(MultiSendIO):
    def __repr__(self) -> str:
        return f"Output(address='{self.address}', coins={self.coins!r})"
