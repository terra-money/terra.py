from __future__ import annotations

import json
from typing import List, Optional, Union

import attr
from terra_proto.cosmwasm.wasm.v1 import AbsoluteTxPosition as AbsoluteTxPosition_pb
from terra_proto.cosmwasm.wasm.v1 import AccessConfig as AccessConfig_pb
from terra_proto.cosmwasm.wasm.v1 import AccessConfigUpdate as AccessConfigUpdate_pb
from terra_proto.cosmwasm.wasm.v1 import AccessType
from terra_proto.cosmwasm.wasm.v1 import AccessTypeParam as AccessTypeParam_pb
from terra_proto.cosmwasm.wasm.v1 import ContractCodeHistoryEntry as HistoryEntry_pb
from terra_proto.cosmwasm.wasm.v1 import ContractCodeHistoryOperationType

from terra_sdk.core.bech32 import AccAddress
from terra_sdk.core.msg import Msg
from terra_sdk.util.json import JSONSerializable

__all__ = ["AccessType", "AccessConfig", "AccessConfigUpdate", "AccessTypeParam"]


def parse_msg(msg: Union[dict, str, bytes]) -> dict:
    if type(msg) is dict:
        return msg
    return json.loads(msg)


def convert_access_type_from_json(access_type: str) -> AccessType:
    if access_type == "Everybody":
        return AccessType.ACCESS_TYPE_EVERYBODY
    elif access_type == "Nobody":
        return AccessType.ACCESS_TYPE_NOBODY
    elif access_type == "OnlyAddress":
        return AccessType.ACCESS_TYPE_ONLY_ADDRESS
    elif access_type == "Unspecified":
        return AccessType.ACCESS_TYPE_UNSPECIFIED


def convert_access_type_to_json(access_type: AccessType) -> str:
    if access_type == AccessType.ACCESS_TYPE_EVERYBODY:
        return AccessType.ACCESS_TYPE_EVERYBODY.name
    elif access_type == AccessType.ACCESS_TYPE_NOBODY:
        return AccessType.ACCESS_TYPE_NOBODY.name
    elif access_type == AccessType.ACCESS_TYPE_ONLY_ADDRESS:
        return AccessType.ACCESS_TYPE_ONLY_ADDRESS.name
    elif access_type == AccessType.ACCESS_TYPE_UNSPECIFIED:
        return AccessType.ACCESS_TYPE_UNSPECIFIED.name


def convert_history_operation_type_to_json(
    operation_type: str,
) -> ContractCodeHistoryOperationType:
    if (
        operation_type
        == ContractCodeHistoryOperationType.CONTRACT_CODE_HISTORY_OPERATION_TYPE_GENESIS
    ):
        return (
            ContractCodeHistoryOperationType.CONTRACT_CODE_HISTORY_OPERATION_TYPE_GENESIS.name
        )
    elif (
        operation_type
        == ContractCodeHistoryOperationType.CONTRACT_CODE_HISTORY_OPERATION_TYPE_INIT
    ):
        return (
            ContractCodeHistoryOperationType.CONTRACT_CODE_HISTORY_OPERATION_TYPE_INIT.name
        )
    elif (
        operation_type
        == ContractCodeHistoryOperationType.CONTRACT_CODE_HISTORY_OPERATION_TYPE_MIGRATE
    ):
        return (
            ContractCodeHistoryOperationType.CONTRACT_CODE_HISTORY_OPERATION_TYPE_MIGRATE.name
        )
    elif (
        operation_type
        == ContractCodeHistoryOperationType.CONTRACT_CODE_HISTORY_OPERATION_TYPE_UNSPECIFIED
    ):
        return (
            ContractCodeHistoryOperationType.CONTRACT_CODE_HISTORY_OPERATION_TYPE_UNSPECIFIED.name
        )


def convert_history_operation_type_from_json(
    operation_type: ContractCodeHistoryOperationType,
) -> str:
    if (
        operation_type
        == ContractCodeHistoryOperationType.CONTRACT_CODE_HISTORY_OPERATION_TYPE_GENESIS.name
    ):
        return (
            ContractCodeHistoryOperationType.CONTRACT_CODE_HISTORY_OPERATION_TYPE_GENESIS
        )
    elif (
        operation_type
        == ContractCodeHistoryOperationType.CONTRACT_CODE_HISTORY_OPERATION_TYPE_INIT.name
    ):
        return (
            ContractCodeHistoryOperationType.CONTRACT_CODE_HISTORY_OPERATION_TYPE_INIT
        )
    elif (
        operation_type
        == ContractCodeHistoryOperationType.CONTRACT_CODE_HISTORY_OPERATION_TYPE_MIGRATE.name
    ):
        return (
            ContractCodeHistoryOperationType.CONTRACT_CODE_HISTORY_OPERATION_TYPE_MIGRATE
        )
    elif (
        operation_type
        == ContractCodeHistoryOperationType.CONTRACT_CODE_HISTORY_OPERATION_TYPE_UNSPECIFIED.name
    ):
        return (
            ContractCodeHistoryOperationType.CONTRACT_CODE_HISTORY_OPERATION_TYPE_UNSPECIFIED
        )


@attr.s
class AccessConfig(JSONSerializable):

    permission: AccessType = attr.ib()
    """"""

    address: AccAddress = attr.ib()
    """"""

    def to_amino(self) -> dict:
        return {
            "permission": convert_access_type_to_json(self.permission),
            "address": self.address,
        }

    def to_data(self) -> dict:
        return {
            "permission": convert_access_type_to_json(self.permission),
            "address": self.address,
        }

    def to_proto(self) -> AccessConfig_pb:
        return AccessConfig_pb(permission=self.permission, address=self.address)

    @classmethod
    def from_data(cls, data: dict) -> AccessConfig:
        return cls(
            permission=convert_access_type_from_json(data["permission"]),
            address=data["address"],
        )

    @classmethod
    def from_proto(cls, proto: AccessConfig_pb) -> AccessConfig:
        return cls(permission=proto.permission, address=proto.address)


@attr.s
class AccessConfigUpdate(JSONSerializable):

    code_id: int = attr.ib()
    """"""

    instantiate_permission: AccessConfig = attr.ib()
    """"""

    def to_amino(self) -> dict:
        return {
            "code_id": self.code_id,
            "instantiate_permission": self.instantiate_permission.to_amino(),
        }

    def to_proto(self) -> AccessConfigUpdate_pb:
        return AccessConfigUpdate_pb(
            code_id=self.code_id,
            instantiate_permission=self.instantiate_permission.to_proto(),
        )

    @classmethod
    def from_data(cls, data: dict) -> AccessConfigUpdate:
        return cls(
            code_id=data["code_id"],
            instantiate_permission=AccessConfig.from_data(
                data["instantiate_permission"]
            )
            if "instantiate_permission" in data
            else None,
        )

    @classmethod
    def from_proto(cls, proto: AccessConfigUpdate_pb) -> AccessConfigUpdate:
        return cls(
            code_id=proto.code_id,
            instantiate_permission=AccessConfig.from_proto(proto.instantiate_permission)
            if proto.instantiate_permission
            else None,
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
            value=self.value,
        )

    @classmethod
    def from_data(cls, data: dict) -> AccessTypeParam:
        return cls(
            value=convert_access_type_from_json(data["value"]),
        )

    @classmethod
    def from_proto(cls, proto: AccessTypeParam_pb) -> AccessTypeParam:
        return cls(value=proto.value)


@attr.s
class AbsoluteTxPosition(JSONSerializable):
    block_height: int = attr.ib()
    tx_index: int = attr.ib()
    """"""

    def to_amino(self):
        return {"block_height": self.block_height, "tx_index": self.tx_index}

    def to_proto(self) -> AbsoluteTxPosition_pb:
        return AbsoluteTxPosition_pb(
            block_height=self.block_height, tx_index=self.tx_index
        )

    @classmethod
    def from_data(cls, data: dict) -> AbsoluteTxPosition:
        return cls(block_height=data["block_height"], tx_index=data["tx_index"])

    @classmethod
    def from_proto(cls, proto: AbsoluteTxPosition_pb) -> AbsoluteTxPosition:
        return cls(block_height=proto.block_height, tx_index=proto.tx_index)


@attr.s
class HistoryEntry(JSONSerializable):
    operation: ContractCodeHistoryOperationType = attr.ib()
    code_id: int = attr.ib()
    updated: Optional[AbsoluteTxPosition] = attr.ib()
    msg: Union[str, dict] = attr.ib()
    """"""

    def to_amino(self):
        return {
            "operation": convert_history_operation_type_to_json(self.operation),
            "code_id": self.code_id,
            "updated": self.updated.to_amino(),
            "msg": self.msg,
        }

    def to_data(self):
        return {
            "operation": convert_history_operation_type_to_json(self.operation),
            "code_id": self.code_id,
            "updated": self.updated.to_data(),
            "msg": self.msg,
        }

    def to_proto(self) -> HistoryEntry_pb:
        return HistoryEntry_pb(
            operation=self.operation,
            code_id=self.code_id,
            updated=self.updated,
            msg=bytes(json.dumps(self.msg), "utf-8"),
        )

    @classmethod
    def from_data(cls, data: dict) -> HistoryEntry:
        return cls(
            operation=convert_history_operation_type_from_json(data["operation"]),
            code_id=data["code_id"],
            updated=AbsoluteTxPosition.from_data(data["updated"])
            if data["updated"]
            else None,
            msg=data["msg"],
        )

    @classmethod
    def from_proto(cls, proto: HistoryEntry_pb) -> HistoryEntry:
        return cls(
            operation=proto.operation,
            code_id=proto.code_id,
            updated=AbsoluteTxPosition.from_proto(proto.updated),
            msg=parse_msg(proto.msg),
        )
