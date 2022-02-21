"""Transaction broadcast result data types."""

from __future__ import annotations

from typing import List, Optional, Union

import attr

from terra_sdk.core.auth import TxLog, parse_tx_logs
from terra_sdk.util.json import JSONSerializable

__all__ = [
    "BlockTxBroadcastResult",
    "SyncTxBroadcastResult",
    "AsyncTxBroadcastResult",
    "is_tx_error",
]


@attr.s
class BlockTxBroadcastResult(JSONSerializable):
    """Data object that contains the response result from node after transaction
    has been broadcasted with the ``block`` broadcast mode."""

    height: int = attr.ib(converter=int)
    """Height at which transaction was included."""
    txhash: str = attr.ib()
    """Transaction hash."""
    raw_log: Optional[str] = attr.ib()
    """Raw JSON of transaction events."""
    gas_wanted: int = attr.ib(converter=int)
    """Gas requested by the transaction."""
    gas_used: int = attr.ib(converter=int)
    """Actual amount of gas consumed by transaction."""
    logs: Optional[List[TxLog]] = attr.ib(converter=parse_tx_logs)  # type: ignore
    """List of transaction logs."""
    code: Optional[int] = attr.ib(default=None)
    """If this is present, the transaction failed."""
    codespace: Optional[str] = attr.ib(default=None)
    """Error subspace name: used alongside ``code``."""
    info: Optional[str] = attr.ib(default=None)
    """"""
    data: Optional[str] = attr.ib(default=None)
    """"""
    timestamp: Optional[str] = attr.ib(default=None)
    """timestamp"""

    def is_tx_error(self) -> bool:
        """Returns whether the transaction failed."""
        return is_tx_error(self)


@attr.s
class SyncTxBroadcastResult(JSONSerializable):
    """Data object that contains the response result from node after transactionco
    has been broadcasted with the ``sync`` broadcast mode."""

    txhash: str = attr.ib()
    """Transaction hash."""
    raw_log: Optional[str] = attr.ib()
    """Raw JSON of transaction events."""
    code: Optional[int] = attr.ib(default=None)
    """If this is present, the transaction failed."""
    codespace: Optional[str] = attr.ib(default=None)
    """Error subspace name: used alongside ``code``."""

    def is_tx_error(self) -> bool:
        """Returns whether the transaction failed."""
        return is_tx_error(self)


@attr.s
class AsyncTxBroadcastResult(JSONSerializable):
    """Data object that contains the response result from node after transaction
    has been broadcasted with the ``sync`` broadcast mode."""

    txhash: str = attr.ib()
    """Transaction hash."""


def is_tx_error(result: Union[BlockTxBroadcastResult, SyncTxBroadcastResult]):
    """Returns whether the transaction failed."""
    return result.code != 0
