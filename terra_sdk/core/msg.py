from __future__ import annotations

from terra_sdk.util.base import BaseTerraData


class Msg(BaseTerraData):
    @staticmethod
    def from_data(data: dict) -> Msg:
        from terra_sdk.util.parse_msg import parse_msg

        return parse_msg(data)
