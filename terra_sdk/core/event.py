"""Serialization of events.
NOTE: Due to lack of consistency throughout Cosmos-SDK and Terra-Core codebases
regarding events, the serialization is very basic and mostly schema-less.

TODO: Make proper event handling middlewares accessible from terra.tx.transformer
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import List

from terra_sdk.util.serdes import terra_sdkBox, JsonDeserializable, JsonSerializable
from terra_sdk.util.validation import Schemas as S

__all__ = ["Event"]

# TODO: Properly treat events in terra-core codebase.

# Example of what event code might look like.
#
# @dataclass
# class MessageEvent:
#
#     type = "message"
#     module: str
#     action: str
#     sender: List[str]
#
#     def __post_init__(self):
#         self.module = self.module[0]
#         self.action = self.action[0]
#
#
# @dataclass
# class TransferEvent:
#
#     type = "transfer"
#     amount: List[Coin]
#     recipient: List[str]
#
#     def __post_init__(self):
#         self.amount = [Coin.from_str(c) for c in self.amount]
#
#
# @dataclass
# class SwapEvent:
#
#     type = "swap"
#     offer: Coin
#     swap_coin: Coin
#     swap_fee: Coin
#     trader: str
#
#     def __post_init__(self):
#         self.offer = Coin.from_str(self.offer[0])
#         self.swap_coin = Coin.from_str(self.swap_coin[0])
#         self.swap_fee = Coin.from_str(self.swap_fee[0])
#         self.trader = self.trader[0]
#
#
# EVENT_TYPES = {
#     "message": MessageEvent,
#     "transfer": TransferEvent,
#     "swap": SwapEvent,
# }


@dataclass
class Event(JsonSerializable, JsonDeserializable):
    __schema__ = S.OBJECT(
        type=S.STRING, attributes=S.ARRAY(S.OBJECT(key=S.STRING, value=S.STRING))
    )

    type: str
    attributes: terra_sdkBox[str, List[str]]

    def __repr__(self) -> str:
        return f"<Event {self.type}>"

    def __getitem__(self, item) -> List[str]:
        return self.attributes[item]

    def __getattr__(self, name) -> List[str]:
        if name in self.attributes:
            return self.attributes[name]
        return self.__getattribute__(name)

    @property
    def pretty_data(self):
        d = {"type": self.type, **self.attributes.to_data()}
        return d.items()

    def to_data(self):
        return {
            "type": self.type,
            "attributes": [
                {"key": k, "value": v} for k, vs in self.attributes.items() for v in vs
            ],
        }

    @classmethod
    def from_data(cls, data: dict) -> Event:
        attrs = defaultdict(list)
        for attr in data["attributes"]:
            attrs[attr["key"]].append(attr["value"])
        return cls(type=data["type"], attributes=terra_sdkBox(attrs))
