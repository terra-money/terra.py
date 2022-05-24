from terra_proto.cosmwasm.wasm.v1 import (
    AccessType, AccessConfig as AccessConfig_pb
)
import attr
from terra_sdk.core.bech32 import AccAddress

from terra_sdk.util.json import JSONSerializable
from terra_sdk.core.msg import Msg

__all__ = [
    "AccessConfig"
]

@attr.s
class AccessConfig(JSONSerializable):
    
    permission: AccessType = attr.ib()
    """"""

    address: AccAddress = attr.ib()
    """"""

    def to_amino(self) -> dict:
        return {
            "permission": self.permission,
            "address": self.address
        }
    
    def to_proto(self) -> AccessConfig_pb:
        return AccessConfig_pb(
            permission=self.permission,
            address=self.address
        )

    @classmethod
    def from_data(cls, data:dict) -> AccessConfig:
        return cls(
            permission=data["permission"],
            address=data["address"]
        )
    
    @classmethod
    def from_proto(cls, proto: AccessConfig_pb) -> AccessConfig_pb:
        return cls(
            permission=proto.permission,
            address=proto.address
        )