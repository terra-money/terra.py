from __future__ import annotations

import attr

from terra_sdk.util.base import BaseMsg

__all__ = ["MsgUnjail"]


@dataclass
class MsgUnjail(BaseMsg):

    type = "cosmos/MsgUnjail"
    action = "unjail"

    address: ValAddress

    @classmethod
    def from_data(cls, data: dict) -> MsgUnjail:
        data = data["value"]
        return cls(address=data["address"])
