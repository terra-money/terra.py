from __future__ import annotations

from terra_sdk.core import Coin, Coins
from terra_sdk.core.msg import Msg

__all__ = ["MsgSend", "MsgMultiSend"]

import attr


@attr.s
class MsgSend(Msg):

    type = "bank/MsgSend"
    action = "send"

    from_address: AccAddress = attr.ib()
    to_address: AccAddress = attr.ib()
    amount: Coins = attr.ib(converter=Coins)

    @classmethod
    def from_data(cls, data: dict) -> MsgSend:
        data = data["value"]
        amount = Coins.from_data(data["amount"])
        return cls(
            from_address=data["from_address"],
            to_address=data["to_address"],
            amount=amount,
        )


@attr.s
class MsgMultiSend(Msg):

    type = "bank/MsgMultiSend"
    action = "multisend"

    inputs = attr.ib()
    outputs = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgMultiSend:
        data = data["value"]
        return cls(
            inputs=[Input.from_data(i) for i in data["inputs"]],
            outputs=[Output.from_data(o) for o in data["outputs"]],
        )
