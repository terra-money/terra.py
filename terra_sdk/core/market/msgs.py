"""Market module message types."""

from __future__ import annotations

import attr
from terra_proto.terra.market.v1beta1 import MsgSwap as MsgSwap_pb
from terra_proto.terra.market.v1beta1 import MsgSwapSend as MsgSwapSend_pb

from terra_sdk.core import AccAddress, Coin
from terra_sdk.core.msg import Msg

__all__ = ["MsgSwap", "MsgSwapSend"]


@attr.s
class MsgSwap(Msg):
    """Perform a native on-chain swap from ``offer_coin`` to ``ask_denom``.

    Args:
        trader: account performing swap
        offer_coin (Union[Coin, str, dict]): coin offered for swap
        ask_denom: denom into which to swap
    """

    type_amino = "market/MsgSwap"
    """"""
    type_url = "/terra.market.v1beta1.MsgSwap"
    """"""
    action = "swap"
    """"""

    trader: AccAddress = attr.ib()
    offer_coin: Coin = attr.ib(converter=Coin.parse)  # type: ignore
    ask_denom: str = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "trader": self.trader,
                "offer_coin": self.offer_coin.to_amino(),
                "ask_denom": self.ask_denom
            }
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgSwap:
        return cls(
            trader=data["trader"],
            offer_coin=Coin.from_data(data["offer_coin"]),
            ask_denom=data["ask_denom"],
        )

    def to_proto(self) -> MsgSwap_pb:
        return MsgSwap_pb(
            trader=self.trader,
            offer_coin=self.offer_coin.to_proto(),
            ask_denom=self.ask_denom,
        )

    @classmethod
    def from_proto(cls, proto: MsgSwap_pb) -> MsgSwap:
        return cls(
            trader=proto.trader,
            offer_coin=Coin.from_proto(proto.offer_coin),
            ask_denom=proto.ask_denom,
        )


@attr.s
class MsgSwapSend(Msg):
    """Performs a swap and sends the resultant swapped amount to ``to_address``.

    Args:
        from_address: account performing swap
        to_address: account which will received resultant funds from swap
        offer_coin (Union[Coin, str, dict]): coin offered for swap
        ask_denom: denom into which to swap
    """

    type_amino = "market/MsgSwapSend"
    """"""
    type_url = "/terra.market.v1beta1.MsgSwapSend"
    """"""
    action = "swapsend"
    """"""

    from_address: AccAddress = attr.ib()
    to_address: AccAddress = attr.ib()
    offer_coin: Coin = attr.ib(converter=Coin.parse)  # type: ignore
    ask_denom: str = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "from_address": self.from_address,
                "to_address": self.to_address,
                "offer_coin": self.offer_coin.to_amino(),
                "ask_denom": self.ask_denom
            }
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgSwapSend:
        return cls(
            from_address=data["from_address"],
            to_address=data["to_address"],
            offer_coin=Coin.from_data(data["offer_coin"]),
            ask_denom=data["ask_denom"],
        )

    def to_proto(self) -> MsgSwapSend_pb:
        return MsgSwapSend_pb(
            from_address=self.from_address,
            to_address=self.to_address,
            offer_coin=self.offer_coin.to_proto(),
            ask_denom=self.ask_denom,
        )

    @classmethod
    def from_proto(cls, proto: MsgSwapSend_pb) -> MsgSwapSend:
        return cls(
            from_address=proto.from_address,
            to_address=proto.to_address,
            offer_coin=Coin.from_proto(proto.offer_coin),
            ask_denom=proto.ask_denom,
        )

