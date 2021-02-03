from __future__ import annotations

import copy
import json
from base64 import b64decode, b64encode

import attr

from terra_sdk.core import AccAddress, Coins
from terra_sdk.core.msg import Msg
from terra_sdk.util.json import dict_to_data

__all__ = [
    "b64_to_dict",
    "dict_to_b64",
    "MsgStoreCode",
    "MsgInstantiateContract",
    "MsgExecuteContract",
    "MsgMigrateContract",
    "MsgUpdateContractOwner",
]


def b64_to_dict(data: str) -> dict:
    """Converts ASCII-encoded base64 encoded string to dict."""
    b64_bytes = data.encode("ascii")
    msg_bytes = b64decode(b64_bytes)
    return json.loads(msg_bytes)


def dict_to_b64(data: dict) -> str:
    """Converts dict to ASCII-encoded base64 encoded string."""
    return b64encode(bytes(json.dumps(data), "ascii")).decode()


@attr.s
class MsgStoreCode(Msg):
    type = "wasm/MsgStoreCode"

    sender: AccAddress = attr.ib()
    wasm_byte_code: str = attr.ib(converter=str)

    @classmethod
    def from_data(cls, data: dict) -> MsgStoreCode:
        data = data["value"]
        return cls(sender=data["sender"], wasm_byte_code=data["wasm_byte_code"])


@attr.s
class MsgInstantiateContract(Msg):
    type = "wasm/MsgInstantiateContract"

    owner: AccAddress = attr.ib()
    code_id: int = attr.ib(converter=int)
    init_msg: dict = attr.ib()
    init_coins: Coins = attr.ib(converter=Coins, factory=Coins)
    migratable: bool = attr.ib(default=False)

    def to_data(self) -> dict:
        d = copy.deepcopy(self.__dict__)
        d["code_id"] = str(d["code_id"])
        d["init_msg"] = dict_to_b64(d["init_msg"])
        return {"type": self.type, "value": dict_to_data(d)}

    @classmethod
    def from_data(cls, data: dict) -> MsgInstantiateContract:
        data = data["value"]
        return cls(
            owner=data["owner"],
            code_id=data["code_id"],
            init_msg=b64_to_dict(data["init_msg"]),
            init_coins=Coins.from_data(data["init_coins"]),
            migratable=data["migratable"],
        )


@attr.s
class MsgExecuteContract(Msg):
    type = "wasm/MsgExecuteContract"

    sender: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()
    execute_msg: dict = attr.ib()
    coins: Coins = attr.ib(converter=Coins, factory=Coins)

    def to_data(self) -> dict:
        d = copy.deepcopy(self.__dict__)
        d["execute_msg"] = dict_to_b64(d["execute_msg"])
        return {"type": self.type, "value": dict_to_data(d)}

    @classmethod
    def from_data(cls, data: dict) -> MsgExecuteContract:
        data = data["value"]
        return cls(
            sender=data["sender"],
            contract=data["contract"],
            execute_msg=b64_to_dict(data["execute_msg"]),
            coins=Coins.from_data(data["coins"]),
        )


@attr.s
class MsgMigrateContract(Msg):
    type = "wasm/MsgExecuteContract"

    owner: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()
    new_code_id: int = attr.ib(converter=int)
    migrate_msg: dict = attr.ib()

    def to_data(self) -> dict:
        d = copy.deepcopy(self.__dict__)
        d["new_code_id"] = str(d["new_code_id"])
        d["migrate_msg"] = dict_to_b64(d["migrate_msg"])
        return {"type": self.type, "value": dict_to_data(d)}

    @classmethod
    def from_data(cls, data: dict) -> MsgMigrateContract:
        data = data["value"]
        return cls(
            owner=data["owner"],
            contract=data["contract"],
            new_code_id=data["new_code_id"],
            migrate_msg=b64_to_dict(data["migrate_msg"]),
        )


@attr.s
class MsgUpdateContractOwner(Msg):
    type = "wasm/MsgUpdateContractOwner"

    owner: AccAddress = attr.ib()
    new_owner: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgUpdateContractOwner:
        data = data["value"]
        return cls(
            owner=data["owner"],
            new_owner=data["new_owner"],
            contract=data["contract"],
        )
