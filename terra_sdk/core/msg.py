from __future__ import annotations

from betterproto.lib.google.protobuf import Any as Any_pb

from terra_sdk.util.base import BaseTerraData


class Msg(BaseTerraData):
    def to_proto(self):
        raise NotImplementedError

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))

    @staticmethod
    def from_data(data: dict) -> Msg:
        from terra_sdk.util.parse_msg import parse_msg

        return parse_msg(data)

    @staticmethod
    def from_proto(proto: any) -> Msg:
        from terra_sdk.util.parse_msg import parse_proto

        return parse_proto(proto)

    @staticmethod
    def unpack_any(any_pb: Any_pb) -> Msg:
        from terra_sdk.util.parse_msg import parse_unpack_any

        return parse_unpack_any(any_pb)
