"Wasm module messages."

from __future__ import annotations

import base64
import json
from cProfile import label
from typing import Optional, Union

import attr
from betterproto.lib.google.protobuf import Any as Any_pb
from terra_proto.cosmwasm.wasm.v1 import MsgClearAdmin as MsgClearAdmin_pb
from terra_proto.cosmwasm.wasm.v1 import MsgExecuteContract as MsgExecuteContract_pb
from terra_proto.cosmwasm.wasm.v1 import (
    MsgInstantiateContract as MsgInstantiateContract_pb,
)
from terra_proto.cosmwasm.wasm.v1 import MsgMigrateContract as MsgMigrateContract_pb
from terra_proto.cosmwasm.wasm.v1 import MsgStoreCode as MsgStoreCode_pb
from terra_proto.cosmwasm.wasm.v1 import MsgUpdateAdmin as MsgUpdateAdmin_pb

from terra_sdk.core import AccAddress, Coins
from terra_sdk.core.msg import Msg
from terra_sdk.core.wasm.data import AccessConfig, AccessTypeParam
from terra_sdk.util.remove_none import remove_none

__all__ = [
    "MsgStoreCode",
    "MsgInstantiateContract",
    "MsgExecuteContract",
    "MsgMigrateContract",
    "MsgUpdateAdmin",
    "MsgClearAdmin",
]


def parse_msg(msg: Union[dict, str, bytes]) -> dict:
    if type(msg) is dict:
        return msg
    return json.loads(msg)


@attr.s
class MsgStoreCode(Msg):
    """Upload a new smart contract WASM binary to the blockchain.

    Args:
        sender: address of sender
        wasm_byte_code: base64-encoded string containing bytecode
        instantiate_permission: access control to apply on contract creation, optional
    """

    type_amino = "wasm/MsgStoreCode"
    """"""
    type_url = "/cosmwasm.wasm.v1.MsgStoreCode"
    """"""
    prototype = MsgStoreCode_pb
    """"""

    sender: AccAddress = attr.ib()
    wasm_byte_code: str = attr.ib()
    instantiate_permission: AccessConfig = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "sender": self.sender,
                "wasm_byte_code": self.wasm_byte_code,
                "instantiate_permission": self.instantiate_permission.to_amino(),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgStoreCode:
        return cls(
            sender=data["sender"],
            wasm_byte_code=data["wasm_byte_code"],
            instantiate_permission=AccessConfig.from_data(
                data["instantiate_permission"]
            ),
        )

    def to_proto(self) -> MsgStoreCode_pb:
        return MsgStoreCode_pb(
            sender=self.sender,
            wasm_byte_code=base64.b64decode(self.wasm_byte_code),
            instantiate_permission=self.instantiate_permission.to_proto(),
        )

    @classmethod
    def from_proto(cls, proto: MsgStoreCode_pb) -> MsgStoreCode:
        return cls(
            sender=proto.sender,
            wasm_byte_code=base64.b64encode(proto.wasm_byte_code).decode(),
            instantiate_permission=AccessConfig.from_proto(
                proto.instantiate_permission
            ),
        )


@attr.s
class MsgInstantiateContract(Msg):
    """Creates a new instance of a smart contract from existing code on the blockchain.

    Args:
        sender: address of sender
        admin: address of contract admin
        code_id (int): code ID to use for instantiation
        label (str): label for the contract.
        msg (dict|str): InitMsg to initialize contract
        funds (Coins): initial amount of coins to be sent to contract
    """

    type_amino = "wasm/MsgInstantiateContract"
    """"""
    type_url = "/cosmwasm.wasm.v1.MsgInstantiateContract"
    """"""
    prototype = MsgInstantiateContract_pb
    """"""

    sender: AccAddress = attr.ib()
    admin: Optional[AccAddress] = attr.ib()
    code_id: int = attr.ib(converter=int)
    label: str = attr.ib(converter=str)
    msg: Union[dict, str] = attr.ib()
    funds: Coins = attr.ib(converter=Coins, factory=Coins)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "sender": self.sender,
                "admin": self.admin,
                "code_id": str(self.code_id),
                "label": self.label,
                "msg": remove_none(self.msg),
                "funds": self.funds.to_amino(),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgInstantiateContract:
        return cls(
            sender=data.get("sender"),
            admin=data.get("admin"),
            code_id=data["code_id"],
            label=data["label"],
            msg=parse_msg(data["msg"]),
            funds=Coins.from_data(data["funds"]),
        )

    def to_proto(self) -> MsgInstantiateContract_pb:
        return MsgInstantiateContract_pb(
            sender=self.sender,
            admin=self.admin,
            code_id=self.code_id,
            label=self.label,
            msg=bytes(json.dumps(self.msg), "utf-8"),
            funds=self.funds.to_proto(),
        )

    @classmethod
    def from_proto(cls, proto: MsgInstantiateContract_pb) -> MsgInstantiateContract:
        return cls(
            sender=proto.sender,
            admin=proto.admin,
            code_id=proto.code_id,
            label=proto.label,
            msg=parse_msg(proto.msg),
            funds=Coins.from_proto(proto.funds),
        )


@attr.s
class MsgExecuteContract(Msg):
    """Execute a state-mutating function on a smart contract.

    Args:
        sender: address of sender
        contract: address of contract to execute function on
        msg (dict|str): ExecuteMsg to pass
        coins: coins to be sent, if needed by contract to execute.
            Defaults to empty ``Coins()``
    """

    type_amino = "wasm/MsgExecuteContract"
    """"""
    type_url = "/cosmwasm.wasm.v1.MsgExecuteContract"
    """"""
    prototype = MsgExecuteContract_pb
    """"""

    sender: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()
    msg: Union[dict, str] = attr.ib()
    coins: Coins = attr.ib(converter=Coins, factory=Coins)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "sender": self.sender,
                "contract": self.contract,
                "msg": remove_none(self.msg),
                "coins": self.coins.to_amino(),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgExecuteContract:
        return cls(
            sender=data["sender"],
            contract=data["contract"],
            msg=parse_msg(data["msg"]),
            coins=Coins.from_data(data["funds"]),
        )

    def to_proto(self) -> MsgExecuteContract_pb:
        return MsgExecuteContract_pb(
            sender=self.sender,
            contract=self.contract,
            msg=bytes(json.dumps(self.msg), "utf-8"),
            funds=self.coins.to_proto(),
        )

    @classmethod
    def from_proto(cls, proto: MsgExecuteContract_pb) -> MsgExecuteContract:
        return cls(
            sender=proto.sender,
            contract=proto.contract,
            msg=parse_msg(proto.msg),
            coins=(proto.funds),
        )


@attr.s
class MsgMigrateContract(Msg):
    """Migrate the contract to a different code ID.

    Args:
        sender: address of contract admin
        contract: address of contract to migrate
        code_id (int): new code ID to migrate to
        msg (dict|str): MigrateMsg to execute
    """

    type_amino = "wasm/MsgMigrateContract"
    """"""
    type_url = "/cosmwasm.wasm.v1.MsgMigrateContract"
    """"""
    prototype = MsgMigrateContract_pb
    """"""

    sender: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()
    code_id: int = attr.ib(converter=int)
    msg: Union[dict, str] = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "sender": self.sender,
                "contract": self.contract,
                "code_id": str(self.code_id),
                "msg": remove_none(self.msg),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgMigrateContract:
        return cls(
            sender=data["sender"],
            contract=data["contract"],
            code_id=data["code_id"],
            msg=parse_msg(data["msg"]),
        )

    def to_proto(self) -> MsgMigrateContract_pb:
        return MsgMigrateContract_pb(
            sender=self.sender,
            contract=self.contract,
            code_id=self.code_id,
            msg=bytes(json.dumps(self.msg), "utf-8"),
        )

    @classmethod
    def from_proto(cls, proto: MsgMigrateContract_pb) -> MsgMigrateContract:
        return cls(
            sender=proto.sender,
            contract=proto.contract,
            code_id=proto.code_id,
            msg=parse_msg(proto.msg),
        )


@attr.s
class MsgUpdateAdmin(Msg):
    """Update a smart contract's admin.

    Args:
        sender: address of current admin (sender)
        new_admin: address of new admin
        contract: address of contract to change
    """

    type_amino = "wasm/MsgUpdateAdmin"
    """"""
    type_url = "/cosmwasm.wasm.v1.MsgUpdateAdmin"
    """"""
    prototype = MsgUpdateAdmin_pb
    """"""

    sender: AccAddress = attr.ib()
    new_admin: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "sender": self.sender,
                "new_admin": self.new_admin,
                "contract": self.contract,
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgUpdateAdmin:
        return cls(
            sender=data["sender"],
            new_admin=data["new_admin"],
            contract=data["contract"],
        )

    def to_proto(self) -> MsgUpdateAdmin_pb:
        return MsgUpdateAdmin_pb(
            sender=self.sender, new_admin=self.new_admin, contract=self.contract
        )

    @classmethod
    def from_proto(cls, proto: MsgUpdateAdmin_pb) -> MsgUpdateAdmin:
        return cls(
            sender=proto.sender,
            new_admin=proto.new_admin,
            contract=proto.contract,
        )


@attr.s
class MsgClearAdmin(Msg):
    """Clears the contract's admin field.

    Args:
        admin: address of current admin (sender)
        contract: address of contract to change
    """

    type_amino = "wasm/MsgClearAdmin"
    """"""
    type_url = "/cosmwasm.wasm.v1.MsgClearAdmin"
    """"""
    prototype = MsgClearAdmin_pb
    """"""

    sender: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {"sender": self.sender, "contract": self.contract},
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgClearAdmin:
        return cls(
            sender=data["sender"],
            contract=data["contract"],
        )

    def to_proto(self) -> MsgClearAdmin_pb:
        return MsgClearAdmin_pb(sender=self.sender, contract=self.contract)

    @classmethod
    def from_proto(cls, proto: MsgClearAdmin_pb) -> MsgClearAdmin:
        return cls(
            sender=proto.sender,
            contract=proto.contract,
        )
