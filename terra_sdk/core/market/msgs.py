from __future__ import annotations

import attr

from terra_sdk.util.base import BaseTerraData


__all__ = ["MsgSwap", "MsgSwapSend"]


@attr.s
class MsgSwap(BaseTerraData):

    type = "market/MsgSwap"
    action = "swap"

    trader: AccAddress = attr.ib()
    offer_coin: Coin = attr.ib()
    ask_denom: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgSwap:
        data = data["value"]
        return cls(
            trader=data["trader"],
            offer_coin=Coin.from_data(data["offer_coin"]),
            ask_denom=data["ask_denom"],
        )
