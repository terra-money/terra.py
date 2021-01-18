from __future__ import annotations

import attr

from terra_sdk.util.base import BaseTerraData

__all__ = [
    "MsgStoreCode",
    "MsgInstantiateContract",
    "MsgExecuteContract",
    "MsgUpdateContractOwner"
]


@attr.s
class MsgStoreCode(BaseTerraData):
    type = 'wasm/MsgStoreCode'

    sender: AccAddress = attr.ib()
    wasm_byte_code: str = attr.ib()


@attr.s
class MsgInstantiateContract(BaseTerraData):
    type = 'wasm/MsgInstantiateContract'

    owner: AccAddress = attr.ib()
    code_id: int = attr.ib()
    init_msg: dict = attr.ib()
    init_coins: Coins = attr.ib()
    migratable: bool = attr.ib()


@attr.s
class MsgExecuteContract(BaseTerraData):
    type = 'wasm/MsgExecuteContract'

    sender: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()
    execute_msg: dict = attr.ib()
    coins: Coins = attr.ib()


@attr.s
class MsgUpdateContractOwner(BaseTerraData):
    type = 'wasm/MsgUpdateContractOwner'

    owner: AccAddress = attr.ib()
    new_owner: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()
