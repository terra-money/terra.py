"Wasm module messages."

from __future__ import annotations

import copy

import attr

from terra_sdk.core import AccAddress, Coins
from terra_sdk.core.msg import Msg
from terra_sdk.util.contract import b64_to_dict, dict_to_b64
from terra_sdk.util.json import dict_to_data

__all__ = [
    "MsgStoreCode",
    "MsgInstantiateContract",
    "MsgExecuteContract",
    "MsgMigrateContract",
    "MsgMigrateCode",
    "MsgUpdateContractAdmin",
    "MsgClearContractAdmin",
]


@attr.s
class MsgStoreCode(Msg):
    """Upload a new smart contract WASM binary to the blockchain.

    Args:
        sender: address of sender
        wasm_byte_code: base64-encoded string containing bytecode
    """

    type = "wasm/MsgStoreCode"
    """"""

    sender: AccAddress = attr.ib()
    wasm_byte_code: str = attr.ib(converter=str)

    @classmethod
    def from_data(cls, data: dict) -> MsgStoreCode:
        data = data["value"]
        return cls(sender=data["sender"], wasm_byte_code=data["wasm_byte_code"])


@attr.s
class MsgInstantiateContract(Msg):
    """Creates a new instance of a smart contract from existing code on the blockchain.

    Args:
        owner: address of contract owner
        code_id (int): code ID to use for instantiation
        init_msg: InitMsg to initialize contract
        init_coins (Coins): initial amount of coins to be sent to contract
        migratable: whether the owner can change contract code IDs"""

    type = "wasm/MsgInstantiateContract"
    """"""

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
    """Execute a state-mutating function on a smart contract.

    Args:
        sender: address of sender
        contract: address of contract to execute function on
        execute_msg: ExecuteMsg (aka. HandleMsg) to pass
        coins: coins to be sent, if needed by contract to execute.
            Defaults to empty ``Coins()``
    """

    type = "wasm/MsgExecuteContract"
    """"""

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
    """Migrate the contract to a different code ID.

    Args:
        owner: address of owner
        contract: address of contract to migrate
        new_code_id (int): new code ID to migrate to
        migrate_msg (dict): MigrateMsg to execute
    """

    type = "wasm/MsgMigrateContract"
    """"""

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
class MsgMigrateCode(Msg):
    """Message to submit Wasm code to the system.

    Args:
        code_id (int): CodeID is the migration target code id
        sender: Sender is the that actor that signed the messages
        wasm_byte_code: WASMByteCode can be raw or gzip compressed
    """

    type = "wasm/MsgMigrateCode"
    """"""

    code_id: int = attr.ib(converter=int)
    sender: AccAddress = attr.ib()
    wasm_byte_code: str = attr.ib(converter=str)

    def to_data(self) -> dict:
        d = copy.deepcopy(self.__dict__)
        d["code_id"] = str(d["new_code_id"])
        return {"type": self.type, "value": dict_to_data(d)}

    @classmethod
    def from_data(cls, data: dict) -> MsgMigrateCode:
        data = data["value"]
        return cls(
            code_id=data["code_id"],
            sender=data["sender"],
            wasm_byte_code=data["wasm_byte_code"],
        )


@attr.s
class MsgUpdateContractAdmin(Msg):
    """Message to set a new admin for a smart contract.

    Args:
        admin: Admin is the current contract admin
        new_admin: NewAdmin is the new contract admin
        contract: Contract is the address of the smart contract
    """

    type = "wasm/MsgUpdateContractAdmin"
    """"""

    admin: AccAddress = attr.ib()
    new_admin: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgUpdateContractAdmin:
        data = data["value"]
        return cls(
            admin=data["admin"],
            new_admin=data["new_admin"],
            contract=data["contract"],
        )


@attr.s
class MsgClearContractAdmin(Msg):
    """Message to clear admin address from a smart contract.

    Args:
        admin: Admin is the current contract admin
        contract: Contract is the address of the smart contract
    """

    type = "wasm/MsgClearContractAdmin"
    """"""

    admin: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgClearContractAdmin:
        data = data["value"]
        return cls(
            admin=data["admin"],
            contract=data["contract"],
        )
