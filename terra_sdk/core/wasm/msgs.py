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


@attr.s
class MsgInstantiateContract(Msg):
    type = "wasm/MsgInstantiateContract"

    owner: AccAddress = attr.ib()
    code_id: int = attr.ib()
    init_msg: dict = attr.ib()
    init_coins: Coins = attr.ib(converter=Coins, factory=Coins)
    migratable: bool = attr.ib(default=False)


@attr.s
class MsgExecuteContract(Msg):
    type = "wasm/MsgExecuteContract"

    sender: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()
    execute_msg: dict = attr.ib()
    coins: Coins = attr.ib(converter=Coins, factory=Coins)


@attr.s
class MsgUpdateContractOwner(Msg):
    type = "wasm/MsgUpdateContractOwner"

    owner: AccAddress = attr.ib()
    new_owner: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()
