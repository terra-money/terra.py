from terra_proto.cosmwasm.wasm.v1 import (
    AccessType,
    AccessConfigUpdate as AccessConfigUpdate_pb,
    AccessTypeParam as AccessTypeParam_pb,
    AccessConfig as AccessConfig_pb
)
import attr
from terra_sdk.core.bech32 import AccAddress

from terra_sdk.util.json import JSONSerializable
from terra_sdk.core.msg import Msg

__all__ = [
    "AccessConfig",
    "AccessConfigUpdate",
    "AccessTypeParam"
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
    def from_proto(cls, proto: AccessConfig_pb) -> AccessConfig:
        return cls(
            permission=proto.permission,
            address=proto.address
        )

@attr.s
class AccessConfigUpdate(JSONSerializable):
    
    code_id: int = attr.ib()
    """"""

    instantiate_permission: AccessConfig = attr.ib()
    """"""

    def to_amino(self) -> dict:
        return {
            "code_id": self.code_id,
            "instantiate_permission": self.instantiate_permission
        }
    
    def to_proto(self) -> AccessConfig_pb:
        return AccessConfig_pb(
            code_id=self.code_id,
            instantiate_permission=self.instantiate_permission
        )

    @classmethod
    def from_data(cls, data:dict) -> AccessConfigUpdate:
        return cls(
            code_id=data["code_id"],
            instantiate_permission=data["instantiate_permission"]
        )
    
    @classmethod
    def from_proto(cls, proto: AccessConfigUpdate_pb) -> AccessConfigUpdate:
        return cls(
            code_id=proto.code_id,
            instantiate_permission=proto.instantiate_permission
        )

@attr.s
class AccessTypeParam(JSONSerializable):
    value: AccessType = attr.ib()
    """"""

    def to_amino(self) -> dict:
        return {
            "value": self.value,
        }
    
    def to_proto(self) -> AccessTypeParam_pb:
        return AccessTypeParam_pb(
            value=self.value,
        )

    @classmethod
    def from_data(cls, data:dict) -> AccessTypeParam:
        return cls(
            value=data["value"],
        )
    
    @classmethod
    def from_proto(cls, proto: AccessTypeParam_pb) -> AccessTypeParam:
        return cls(
            value=proto.value
        )
