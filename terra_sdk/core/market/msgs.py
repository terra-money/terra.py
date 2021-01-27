from __future__ import annotations

import attr

from terra_sdk.core.msg import Msg


__all__ = ["MsgSwap", "MsgSwapSend"]


@attr.s
class MsgSwap(Msg):

    type = "market/MsgSwap"
    action = "swap"

    trader: AccAddress = attr.ib()
    offer_coin: Coin = attr.ib(converter=Coin.parse)
    ask_denom: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgSwap:
        data = data["value"]
        return cls(
            trader=data["trader"],
            offer_coin=Coin.from_data(data["offer_coin"]),
            ask_denom=data["ask_denom"],
        )
