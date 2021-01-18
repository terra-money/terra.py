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


@attr.s
class MsgInstantiateContract(BaseTerraData):
    type = 'wasm/MsgInstantiateContract'


@attr.s
class MsgExecuteContract(BaseTerraData):
    type = 'wasm/MsgExecuteContract'


@attr.s
class MsgUpdateContractOwner(BaseTerraData):
    type = 'wasm/MsgUpdateContractOwner'
