from __future__ import annotations

from abc import abstractmethod

from betterproto.lib.google.protobuf import Any

from terra_sdk.util.base import BaseTerraData
from betterproto import Message

class Msg(BaseTerraData, Message):

    @abstractmethod
    def pack_any(self) -> Any:
        raise NotImplementedError

    @staticmethod
    def from_data(data: dict) -> Msg:
        from terra_sdk.util.parse_msg import parse_msg

        return parse_msg(data)
