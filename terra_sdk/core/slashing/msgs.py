from __future__ import annotations

from dataclasses import dataclass

from terra_sdk.core import ValAddress
from terra_sdk.core.msg import StdMsg
from terra_sdk.util.validation import Schemas as S
from terra_sdk.util.validation import validate_val_address

__all__ = ["MsgUnjail"]


@dataclass
class MsgUnjail(StdMsg):

    type = "cosmos/MsgUnjail"
    action = "unjail"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^cosmos/MsgUnjail\Z"),
        value=S.OBJECT(address=S.VAL_ADDRESS),
    )

    address: ValAddress

    def __post_init__(self):
        self.address = validate_val_address(self.address)

    @classmethod
    def from_data(cls, data: dict) -> MsgUnjail:
        data = data["value"]
        return cls(address=data["address"])
