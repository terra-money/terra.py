from __future__ import annotations

from terra_sdk.core import AccAddress, Coins
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
        return cls(
            from_address=data["from_address"],
            to_address=data["to_address"],
            amount=Coins.from_data(data["amount"]),
        )


@attr.s
class MsgMultiSend(Msg):

    type = "bank/MsgMultiSend"
    action = "multisend"

    # TODO: improve interface - match terra.js
    inputs = attr.ib()
    outputs = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgMultiSend:
        data = data["value"]
        return cls(
            inputs=data["inputs"],
            outputs=data["outputs"],
        )
