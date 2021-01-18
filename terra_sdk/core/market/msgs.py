from __future__ import annotations

from dataclasses import dataclass

from terra_sdk.core import AccAddress, Coin
from terra_sdk.core.msg import StdMsg
from terra_sdk.util.validation import Schemas as S
from terra_sdk.util.validation import validate_acc_address

__all__ = ["MsgSwap"]


@dataclass
class MsgSwap(StdMsg):

    type = "market/MsgSwap"
    action = "swap"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^market/MsgSwap\Z"),
        value=S.OBJECT(
            trader=S.ACC_ADDRESS, offer_coin=Coin.__schema__, ask_denom=S.STRING
        ),
    )

    trader: AccAddress
    offer_coin: Coin
    ask_denom: str

    def __post_init__(self):
        self.trader = validate_acc_address(self.trader)

    @classmethod
    def from_data(cls, data: dict) -> MsgSwap:
        data = data["value"]
        return cls(
            trader=data["trader"],
            offer_coin=Coin.from_data(data["offer_coin"]),
            ask_denom=data["ask_denom"],
        )
