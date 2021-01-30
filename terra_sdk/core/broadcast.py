from __future__ import annotations

import attr
from terra_sdk.core.auth import TxLog
from terra_sdk.util.json import JSONSerializable


@attr.s
class BlockTxBroadcastResult(JSONSerializable):

    height: int = attr.ib(converter=int)
    txhash: str = attr.ib()
    raw_log: str = attr.ib()
    gas_wanted: int = attr.ib(converter=int)
    gas_used: int = attr.ib(converter=int)
    logs: Optional[List[TxLog]] = attr.ib(
        converter=lambda logs: [TxLog(**l) for l in logs] if logs else None
    )
    code: Optional[int] = attr.ib(default=None)
    codespace: Optional[str] = attr.ib(default=None)


@attr.s
class SyncTxBroadcastResult(JSONSerializable):

    height: int = attr.ib(converter=int)
    txhash: str = attr.ib()
    raw_log: str = attr.ib()
    code: Optional[int] = attr.ib(default=None)
    codespace: Optional[str] = attr.ib(default=None)


@attr.s
class AsyncTxBroadcastResult(JSONSerializable):

    height: int = attr.ib(converter=int)
    txhash: str = attr.ib()