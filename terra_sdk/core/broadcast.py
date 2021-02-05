from __future__ import annotations

from typing import List, Optional, Union

import attr

from terra_sdk.core.auth import TxLog, parse_tx_logs
from terra_sdk.util.json import JSONSerializable

__all__ = ["BlockTxBroadcastResult", "SyncTxBroadcastResult", "AsyncTxBroadcastResult"]


@attr.s
class BlockTxBroadcastResult(JSONSerializable):

    height: int = attr.ib(converter=int)
    txhash: str = attr.ib()
    raw_log: str = attr.ib()
    gas_wanted: int = attr.ib(converter=int)
    gas_used: int = attr.ib(converter=int)
    logs: Optional[List[TxLog]] = attr.ib(converter=parse_tx_logs)  # type: ignore
    code: Optional[int] = attr.ib(default=None)
    codespace: Optional[str] = attr.ib(default=None)

    def is_tx_error(self) -> bool:
        return is_tx_error(self)


@attr.s
class SyncTxBroadcastResult(JSONSerializable):

    height: int = attr.ib(converter=int)
    txhash: str = attr.ib()
    raw_log: str = attr.ib()
    code: Optional[int] = attr.ib(default=None)
    codespace: Optional[str] = attr.ib(default=None)

    def is_tx_error(self) -> bool:
        return is_tx_error(self)


@attr.s
class AsyncTxBroadcastResult(JSONSerializable):

    height: int = attr.ib(converter=int)
    txhash: str = attr.ib()


def is_tx_error(result: Union[BlockTxBroadcastResult, SyncTxBroadcastResult]):
    return result.code is not None
