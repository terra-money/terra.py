from __future__ import annotations

import attr

from terra_sdk.core.msg import Msg

__all__ = [
    "MsgStoreCode",
    "MsgInstantiateContract",
    "MsgExecuteContract",
    "MsgUpdateContractOwner",
]


@attr.s
class MsgStoreCode(Msg):
    type = "wasm/MsgStoreCode"

    sender: AccAddress = attr.ib()
    wasm_byte_code: str = attr.ib()

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

    def object_value(self):
        c = copy.deepcopy(self.__dict__)
        c["code_id"] = str(c["code_id"])
        return c

    @classmethod
    def from_data(cls, data: dict) -> MsgInstantiateContract:
        data = data["value"]
        return cls(
            owner=data["owner"],
            code_id=data["code_id"],
            init_msg=data["init_msg"],
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

    @classmethod
    def from_data(cls, data: dict) -> MsgExecuteContract:
        data = data["value"]
        return cls(
            sender=data["sender"],
            contract=data["contract"],
            execute_msg=data["execute_msg"],
            coins=Coins.from_data(data["coins"]),
        )


@attr.s
class MsgMigrateContract(Msg):
    type = "wasm/MsgExecuteContract"

    owner: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()
    new_code_id: int = attr.ib(converter=int)
    migrate_msg: dict = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgExecuteContract:
        data = data["value"]
        return cls(
            owner=data["owner"],
            contract=data["contract"],
            new_code_id=data["new_code_id"],
            migrate_msg=data["migrate_msg"],
        )


@attr.s
class MsgUpdateContractOwner(Msg):
    type = "wasm/MsgUpdateContractOwner"

    owner: AccAddress = attr.ib()
    new_owner: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgExecuteContract:
        data = data["value"]
        return cls(
            owner=data["owner"],
            new_owner=data["new_owner"],
            contract=data["contract"],
        )


@attr.s
class MsgUpdateContractOwner(Msg):
    type = "wasm/MsgUpdateContractOwner"

    owner: AccAddress = attr.ib()
    new_owner: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgExecuteContract:
        data = data["value"]
        return cls(
            owner=data["owner"],
            new_owner=data["new_owner"],
            contract=data["contract"],
        )
