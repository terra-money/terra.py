from __future__ import annotations

from typing import Iterable, Union

from terra_sdk.core.auth.transaction import TxInfo
from terra_sdk.query.msginfo import MsgInfosQuery
from terra_sdk.util.pretty import PrettyPrintable, pretty_repr

__all__ = ["TxInfosQuery"]


class TxInfosQuery(PrettyPrintable):
    def __init__(self, txinfos: Iterable[TxInfo]):
        self.txinfos = list(txinfos)

    def __repr__(self) -> str:
        return f"<TxInfosQuery {len(self.txinfos)} txs, {len(self.msgs)} msgs>"

    def __getitem__(self, key) -> Union[TxInfo, TxInfosQuery]:
        if isinstance(key, int):
            return self.txinfos[key]
        elif isinstance(key, slice):
            return TxInfosQuery(self.txinfos[key])
        else:
            raise KeyError(
                f"unusuable key {key} for TxInfosQuery (use 'int' or 'slice')"
            )

    def __len__(self) -> int:
        return len(self.txinfos)

    @property
    def msgs(self) -> MsgInfosQuery:
        return MsgInfosQuery([msg for t in self.txinfos for msg in t.msgs])

    @property
    def pretty_iterable(self) -> bool:
        return True

    def _pretty_repr_(self, path: str = "") -> str:
        return pretty_repr(self.txinfos, path)
