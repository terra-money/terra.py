from __future__ import annotations

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
    "AccessType",
    "AccessConfig",
    "AccessConfigUpdate",
    "AccessTypeParam"
]


def convert_access_type_from_json(access_type : str) -> AccessType :
    if access_type == 'Everybody' :
        return AccessType.ACCESS_TYPE_EVERYBODY
    elif access_type == 'Nobody'   :
        return AccessType.ACCESS_TYPE_NOBODY
    elif access_type == 'OnlyAddress' :
        return AccessType.ACCESS_TYPE_ONLY_ADDRESS
    elif access_type == 'Unspecified' :
        return AccessType.ACCESS_TYPE_UNSPECIFIED

def convert_access_type_to_json(access_type : AccessType) -> str :
    if access_type == AccessType.ACCESS_TYPE_EVERYBODY :
        return 'Everybody' 
    elif access_type == AccessType.ACCESS_TYPE_NOBODY   :
        return 'Nobody'
    elif access_type == AccessType.ACCESS_TYPE_ONLY_ADDRESS :
        return 'OnlyAddress'
    elif access_type == AccessType.ACCESS_TYPE_UNSPECIFIED :
        return 'Unspecified'

@attr.s
class AccessConfig(JSONSerializable):
    
    permission: AccessType = attr.ib()
    """"""

    address: AccAddress = attr.ib()
    """"""

    def to_amino(self) -> dict:
        return {
            "permission": convert_access_type_to_json(self.permission),
            "address": self.address
        }
    
    def to_data(self) -> dict:
        return {
            "permission": convert_access_type_to_json(self.permission),
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
            permission=convert_access_type_from_json(data["permission"]) ,
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
            "instantiate_permission": self.instantiate_permission.to_amino()
        }
        
    
    def to_proto(self) -> AccessConfigUpdate_pb:
        return AccessConfigUpdate_pb(
            code_id=self.code_id,
            instantiate_permission=self.instantiate_permission.to_proto()
        )

    @classmethod
    def from_data(cls, data:dict) -> AccessConfigUpdate:
        return cls(
            code_id=data["code_id"],
            instantiate_permission=AccessConfig.from_data(data["instantiate_permission"]) if "instantiate_permission" in data else None
        )
    
    @classmethod
    def from_proto(cls, proto: AccessConfigUpdate_pb) -> AccessConfigUpdate:
        return cls(
            code_id=proto.code_id,
            instantiate_permission=AccessConfig.from_proto(proto.instantiate_permission) if proto.instantiate_permission else None
        )

@attr.s
class AccessTypeParam(JSONSerializable):
    value: AccessType = attr.ib()
    """"""

    def to_amino(self) -> dict:
        return {
            "value": convert_access_type_to_json(self.value),
        }
    
    def to_proto(self) -> AccessTypeParam_pb:
        return AccessTypeParam_pb(
            value= self.value,
        )

    @classmethod
    def from_data(cls, data:dict) -> AccessTypeParam:
        return cls(
            value= convert_access_type_from_json(data["value"]),
        )
    
    @classmethod
    def from_proto(cls, proto: AccessTypeParam_pb) -> AccessTypeParam:
        return cls(
            value=proto.value
        )
