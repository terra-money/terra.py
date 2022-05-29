"""wasm module governance proposal types."""

from __future__ import annotations

import base64
import json
from copyreg import add_extension
from curses import init_color
from typing import List, Union

import attr
from betterproto.lib.google.protobuf import Any as Any_pb
from terra_proto.cosmwasm.wasm.v1 import ClearAdminProposal as ClearAdminProposal_pb
from terra_proto.cosmwasm.wasm.v1 import (
    ExecuteContractProposal as ExecuteContractProposal_pb,
)
from terra_proto.cosmwasm.wasm.v1 import (
    InstantiateContractProposal as InstantiateContractProposal_pb,
)
from terra_proto.cosmwasm.wasm.v1 import (
    MigrateContractProposal as MigrateContractProposal_pb,
)
from terra_proto.cosmwasm.wasm.v1 import PinCodesProposal as PinCodesProposal_pb
from terra_proto.cosmwasm.wasm.v1 import StoreCodeProposal as StoreCodeProposal_pb
from terra_proto.cosmwasm.wasm.v1 import SudoContractProposal as SudoContractProposal_pb
from terra_proto.cosmwasm.wasm.v1 import UnpinCodesProposal as UnpinCodesProposal_pb
from terra_proto.cosmwasm.wasm.v1 import UpdateAdminProposal as UpdateAdminProposal_pb
from terra_proto.cosmwasm.wasm.v1 import (
    UpdateInstantiateConfigProposal as UpdateInstantiateConfigProposal_pb,
)

from terra_sdk.core.bech32 import AccAddress
from terra_sdk.core.coins import Coins
from terra_sdk.core.wasm.data import AccessConfig, AccessConfigUpdate
from terra_sdk.util.json import JSONSerializable
from terra_sdk.util.remove_none import remove_none

__all__ = [
    "ClearAdminProposal",
    "ExecuteContractProposal",
    "InstantiateContractProposal",
    "MigrateContractProposal",
    "PinCodesProposal",
    "StoreCodeProposal",
    "SudoContractProposal",
    "UnpinCodesProposal",
    "UpdateAdminProposal",
    "UpdateInstantiateConfigProposal",
]


def parse_msg(msg: Union[dict, str, bytes]) -> dict:
    if type(msg) is dict:
        return msg
    return json.loads(msg)


@attr.s
class ClearAdminProposal(JSONSerializable):
    """
    Args:
        title : a short summary
        description : a human readable text
        contract : the address of the smart contract
    """

    type_amino = "wasm/ClearAdminProposal"
    type_url = "/cosmwasm.wasm.v1.ClearAdminProposal"

    title: str = attr.ib()
    description: str = attr.ib()
    contract: AccAddress = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "title": self.title,
                "description": self.description,
                "contract": self.contract,
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "title": self.title,
            "description": self.description,
            "contract": self.contract,
        }

    def to_proto(self) -> ClearAdminProposal:
        return ClearAdminProposal_pb(
            title=self.title, description=self.description, contract=self.contract
        )

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))

    @classmethod
    def from_data(cls, data):
        return cls(
            title=data["title"],
            description=data["description"],
            contract=data["contract"],
        )

    @classmethod
    def from_proto(cls, proto: ClearAdminProposal_pb):
        return cls(
            title=proto.title, description=proto.description, contract=proto.contract
        )


@attr.s
class ExecuteContractProposal(JSONSerializable):
    """
    Args:
        title : a short summary
        description : a human readable text
        run_as : contract user
        contract : the address of the smart contract
        execute_msg : HandleMsg to pass as arguments for contract invocation
        coins : coins to be sent to contract
    """

    type_amino = "wasm/ExecuteContractProposal"
    type_url = "/cosmwasm.wasm.v1.ExecuteContractProposal"
    prototype = ExecuteContractProposal_pb

    title: str = attr.ib()
    description: str = attr.ib()
    run_as: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()
    execute_msg: Union[dict, str] = attr.ib()
    coins: Coins = attr.ib(converter=Coins, factory=Coins)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "title": self.title,
                "description": self.description,
                "run_as": self.run_as,
                "contract": self.contract,
                "execute_msg": remove_none(self.execute_msg),
                "coins": self.coins.to_amino(),
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "title": self.title,
            "description": self.description,
            "run_as": self.run_as,
            "contract": self.contract,
            "execute_msg": remove_none(self.execute_msg),
            "coins": self.coins.to_data(),
        }

    def to_proto(self) -> ExecuteContractProposal:
        return ExecuteContractProposal_pb(
            title=self.title,
            description=self.description,
            run_as=self.run_as,
            contract=self.contract,
            execute_msg=bytes(json.dumps(self.execute_msg), "utf-8"),
            coins=self.coins.to_proto(),
        )

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))

    @classmethod
    def from_data(cls, data):
        return cls(
            title=data["title"],
            description=data["description"],
            run_as=data["run_as"],
            contract=data["contract"],
            execute_msg=parse_msg(data["execute_msg"]),
            coins=Coins.from_data(data["coins"]),
        )

    @classmethod
    def from_proto(cls, proto: ExecuteContractProposal_pb):
        return cls(
            title=proto.title,
            description=proto.description,
            run_as=proto.run_as,
            contract=proto.contract,
            execute_msg=parse_msg(proto.msg),
            coins=Coins.from_proto(proto.funds),
        )


@attr.s
class InstantiateContractProposal(JSONSerializable):
    """
    Args:
        title : a short summary
        description : a human readable text
        run_as : contract user
        admin : an optional contract admin address who can migrate the contract, put empty string to disable migration
        code_id : the reference to the stored WASM code
        init_msg : json encoded message to be passed to the contract on instantiation
        init_coins : transferred to the contract on execution
        label : label for the contract. v2 supported only
    """

    type_amino = "wasm/InstantiateContractProposal"
    type_url = "/cosmwasm.wasm.v1.InstantiateContractProposal"
    prototype = InstantiateContractProposal_pb

    title: str = attr.ib()
    description: str = attr.ib()
    run_as: AccAddress = attr.ib()
    admin: Union[AccAddress, None] = attr.ib()
    code_id: int = attr.ib()
    init_msg: Union[dict, str] = attr.ib()
    init_coins: Coins = attr.ib(converter=Coins)
    label: str = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "title": self.title,
                "description": self.description,
                "run_as": self.run_as,
                "admin": self.admin,
                "code_id": self.code_id,
                "init_msg": remove_none(self.init_msg),
                "init_coins": self.init_coins.to_amino(),
                "label": self.label,
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "title": self.title,
            "description": self.description,
            "run_as": self.run_as,
            "admin": self.admin,
            "code_id": self.code_id,
            "init_msg": remove_none(self.init_msg),
            "init_coins": self.init_coins.to_amino(),
            "label": self.label,
        }

    def to_proto(self) -> InstantiateContractProposal:
        return InstantiateContractProposal_pb(
            title=self.title,
            description=self.description,
            run_as=self.run_as,
            admin=self.admin,
            code_id=self.code_id,
            init_msg=bytes(json.dumps(self.init_msg), "utf-8"),
            init_coins=self.init_coins.to_proto(),
            label=self.label,
        )

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))

    @classmethod
    def from_data(cls, data):
        return cls(
            title=data["title"],
            description=data["description"],
            run_as=data["run_as"],
            admin=data["admin"],
            code_id=data["code_id"],
            init_msg=parse_msg(data["init_msg"]),
            init_coins=Coins.from_data(data["init_coins"]),
            label=data["label"],
        )

    @classmethod
    def from_proto(cls, proto: InstantiateContractProposal_pb):
        return cls(
            title=proto.title,
            description=proto.description,
            run_as=proto.run_as,
            admin=proto.admin,
            code_id=proto.code_id,
            init_msg=parse_msg(proto.msg),
            init_coins=Coins.from_proto(proto.funds),
            label=proto.label,
        )


@attr.s
class MigrateContractProposal(JSONSerializable):
    """
    Args:
        title : a short summary
        description : a human readable text
        contract : contract address to be migrated from
        new_code_id : reference to the new code on the blockchain
        migrate_msg : JSON message to configure the migrate state of the contract
    """

    type_amino = "wasm/MigrateContractProposal"
    type_url = "/cosmwasm.wasm.v1.MigrateContractProposal"
    prototype = MigrateContractProposal_pb

    title: str = attr.ib()
    description: str = attr.ib()
    contract: AccAddress = attr.ib()
    new_code_id: int = attr.ib()
    migrate_msg: Union[dict, str] = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "title": self.title,
                "description": self.description,
                "contract": self.contract,
                "new_code_id": self.new_code_id,
                "migrate_msg": remove_none(self.migrate_msg),
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "title": self.title,
            "description": self.description,
            "contract": self.contract,
            "new_code_id": self.new_code_id,
            "migrate_msg": remove_none(self.migrate_msg),
        }

    def to_proto(self) -> MigrateContractProposal:
        return MigrateContractProposal_pb(
            title=self.title,
            description=self.description,
            contract=self.contract,
            new_code_id=self.new_code_id,
            migrate_msg=bytes(json.dumps(self.migrate_msg), "utf-8"),
        )

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))

    @classmethod
    def from_data(cls, data):
        return cls(
            title=data["title"],
            description=data["description"],
            contract=data["contract"],
            new_code_id=data["new_code_id"],
            migrate_msg=parse_msg(data["migrate_msg"]),
        )

    @classmethod
    def from_proto(cls, proto: MigrateContractProposal_pb):
        return cls(
            title=proto.title,
            description=proto.description,
            contract=proto.contract,
            new_code_id=proto.code_id,
            migrate_msg=parse_msg(proto.msg),
        )


@attr.s
class PinCodesProposal(JSONSerializable):
    """
    Args:
        title : a short summary
        description : a human readable text
        code_ids : the address of the smart code_ids
    """

    type_amino = "wasm/PinCodesProposal"
    type_url = "/cosmwasm.wasm.v1.PinCodesProposal"

    title: str = attr.ib()
    description: str = attr.ib()
    code_ids: List[int] = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "title": self.title,
                "description": self.description,
                "code_ids": [code_id for code_id in self.code_ids],
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "title": self.title,
            "description": self.description,
            "code_ids": [code_id for code_id in self.code_ids],
        }

    def to_proto(self) -> PinCodesProposal:
        return PinCodesProposal_pb(
            title=self.title,
            description=self.description,
            code_ids=[code_id for code_id in self.code_ids],
        )

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))

    @classmethod
    def from_data(cls, data):
        return cls(
            title=data["title"],
            description=data["description"],
            code_ids=[code_id for code_id in data["code_ids"]],
        )

    @classmethod
    def from_proto(cls, proto: PinCodesProposal_pb):
        return cls(
            title=proto.title,
            description=proto.description,
            code_ids=[code_id for code_id in proto.code_ids],
        )


@attr.s
class StoreCodeProposal(JSONSerializable):
    """
    Args:
        title : a short summary
        description : a human readable text
        run_as : the address that is passed to the contract's environment as sender
        wasm_byte_code : can be raw or gzip compressed
        instantiate_permission : to apply on contract creation, optional
    """

    type_amino = "wasm/StoreCodeProposal"
    type_url = "/cosmwasm.wasm.v1.StoreCodeProposal"

    title: str = attr.ib()
    description: str = attr.ib()
    run_as: str = attr.ib()
    wasm_byte_code: str = attr.ib()
    instantiate_permission: AccessConfig = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "title": self.title,
                "description": self.description,
                "run_as": self.run_as,
                "wasm_byte_code": self.wasm_byte_code,
                "instantiate_permission": self.instantiate_permission.to_amino(),
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "title": self.title,
            "description": self.description,
            "run_as": self.run_as,
            "wasm_byte_code": self.wasm_byte_code,
            "instantiate_permission": self.instantiate_permission.to_data(),
        }

    def to_proto(self) -> StoreCodeProposal:
        return StoreCodeProposal_pb(
            title=self.title,
            description=self.description,
            run_as=self.run_as,
            wasm_byte_code=base64.b64encode(self.wasm_byte_code),
            instantiate_permission=self.instantiate_permission,
        )

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))

    @classmethod
    def from_data(cls, data):
        return cls(
            title=data["title"],
            description=data["description"],
            run_as=data["run_as"],
            wasm_byte_code=data["wasm_byte_code"],
            instantiate_permission=AccessConfig.from_data(
                data["instantiate_permission"]
            ),
        )

    @classmethod
    def from_proto(cls, proto: StoreCodeProposal_pb):
        return cls(
            title=proto.title,
            description=proto.description,
            run_as=proto.run_as,
            wasm_byte_code=base64.b64encode(proto.wasm_byte_code).decode(),
            instantiate_permission=AccessConfig.from_proto(
                proto.instantiate_permission
            ),
        )


@attr.s
class SudoContractProposal(JSONSerializable):
    """
    Args:
        title : a short summary
        description : a human readable text
        contract :  contract address to be migrated from
        msg : JSON message to configure the migrate state of the contract
    """

    type_amino = "wasm/SudoContractProposal"
    type_url = "/cosmwasm.wasm.v1.SudoContractProposal"

    title: str = attr.ib()
    description: str = attr.ib()
    contract: AccAddress = attr.ib()
    msg: Union[dict, str] = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "title": self.title,
                "description": self.description,
                "contract": self.contract,
                "msg": remove_none(self.msg),
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "title": self.title,
            "description": self.description,
            "contract": self.contract,
            "msg": remove_none(self.msg),
        }

    def to_proto(self) -> SudoContractProposal:
        return SudoContractProposal_pb(
            title=self.title,
            description=self.description,
            contract=self.contract,
            msg=bytes(json.dumps(self.msg), "utf-8"),
        )

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))

    @classmethod
    def from_data(cls, data):
        return cls(
            title=data["title"],
            description=data["description"],
            contract=data["contract"],
            msg=parse_msg(data["msg"]),
        )

    @classmethod
    def from_proto(cls, proto: SudoContractProposal_pb):
        return cls(
            title=proto.title,
            description=proto.description,
            contract=proto.contract,
            msg=parse_msg(proto.msg),
        )


@attr.s
class UnpinCodesProposal(JSONSerializable):
    """
    Args:
        title : a short summary
        description : a human readable text
        code_ids : the address of the smart code_ids
    """

    type_amino = "wasm/UnpinCodesProposal"
    type_url = "/cosmwasm.wasm.v1.UnpinCodesProposal"

    title: str = attr.ib()
    description: str = attr.ib()
    code_ids: List[int] = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "title": self.title,
                "description": self.description,
                "code_ids": [code_id for code_id in self.code_ids],
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "title": self.title,
            "description": self.description,
            "code_ids": [code_id for code_id in self.code_ids],
        }

    def to_proto(self) -> UnpinCodesProposal:
        return UnpinCodesProposal_pb(
            title=self.title,
            description=self.description,
            code_ids=[code_id for code_id in self.code_ids],
        )

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))

    @classmethod
    def from_data(cls, data):
        return cls(
            title=data["title"],
            description=data["description"],
            code_ids=[code_id for code_id in data["code_ids"]],
        )

    @classmethod
    def from_proto(cls, proto: UnpinCodesProposal_pb):
        return cls(
            title=proto.title,
            description=proto.description,
            code_ids=[code_id for code_id in proto.code_ids],
        )


@attr.s
class UpdateAdminProposal(JSONSerializable):
    """
    Args:
        title : a short summary
        description : a human readable text
        contract : the address of the smart contract
        new_admin : address to be set
    """

    type_amino = "wasm/UpdateAdminProposal"
    type_url = "/cosmwasm.wasm.v1.UpdateAdminProposal"

    title: str = attr.ib()
    description: str = attr.ib()
    contract: AccAddress = attr.ib()
    new_admin: AccAddress = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "title": self.title,
                "description": self.description,
                "contract": self.contract,
                "new_admin": self.new_admin,
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "title": self.title,
            "description": self.description,
            "contract": self.contract,
            "new_admin": self.new_admin,
        }

    def to_proto(self) -> UpdateAdminProposal:
        return UpdateAdminProposal_pb(
            title=self.title,
            description=self.description,
            contract=self.contract,
            new_admin=self.new_admin,
        )

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))

    @classmethod
    def from_data(cls, data):
        return cls(
            title=data["title"],
            description=data["description"],
            contract=data["contract"],
            new_admin=data["new_admin"],
        )

    @classmethod
    def from_proto(cls, proto: UpdateAdminProposal_pb):
        return cls(
            title=proto.title,
            description=proto.description,
            contract=proto.contract,
            new_admin=proto.new_admin,
        )


@attr.s
class UpdateInstantiateConfigProposal(JSONSerializable):
    """
    Args:
        title : a short summary
        description : a human readable text
        access_config_updates : the address of the smart access_config_updates
    """

    type_amino = "wasm/UpdateInstantiateConfigProposal"
    type_url = "/cosmwasm.wasm.v1.UpdateInstantiateConfigProposal"

    title: str = attr.ib()
    description: str = attr.ib()
    access_config_updates: List[AccessConfigUpdate] = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "title": self.title,
                "description": self.description,
                "access_config_updates": [
                    access_config_update.to_amino()
                    for access_config_update in self.access_config_updates
                ],
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "title": self.title,
            "description": self.description,
            "access_config_updates": [
                access_config_update.to_data()
                for access_config_update in self.access_config_updates
            ],
        }

    def to_proto(self) -> UpdateInstantiateConfigProposal:
        return UpdateInstantiateConfigProposal_pb(
            title=self.title,
            description=self.description,
            access_config_updates=[
                access_config_update.to_proto()
                for access_config_update in self.access_config_updates
            ],
        )

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))

    @classmethod
    def from_data(cls, data):
        return cls(
            title=data["title"],
            description=data["description"],
            access_config_updates=[
                AccessConfigUpdate.from_data(access_config_update)
                for access_config_update in data["access_config_updates"]
            ],
        )

    @classmethod
    def from_proto(cls, proto: UpdateInstantiateConfigProposal_pb):
        return cls(
            title=proto.title,
            description=proto.description,
            access_config_updates=[
                AccessConfigUpdate.from_proto(access_config_update)
                for access_config_update in proto.access_config_updates
            ],
        )
