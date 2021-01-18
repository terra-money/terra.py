from __future__ import annotations

import attr

from terra_sdk.util.base import BaseTerraData

__all__ = ["MsgUnjail"]


@dataclass
class MsgUnjail(BaseTerraData):

    type = "cosmos/MsgUnjail"
    action = "unjail"

    address: ValAddress

    @classmethod
    def from_data(cls, data: dict) -> MsgUnjail:
        data = data["value"]
        return cls(address=data["address"])
