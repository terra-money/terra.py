from __future__ import annotations

from typing import Dict, List, Optional

import attr

from terra_sdk.core.coins import Coins
from terra_sdk.core.msg import Msg
from terra_sdk.core.public_key import PublicKey
from terra_sdk.util.json import JSONSerializable

__all__ = [
    "StdSignature",
    "StdFee",
    "StdSignMsg",
    "StdTx",
    "TxLog",
    "TxInfo",
    "parse_tx_logs",
]


@attr.s
class StdSignature(JSONSerializable):

    signature: str = attr.ib()
    pub_key: Optional[PublicKey] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> StdSignature:
        return cls(
            signature=data["signature"],
            pub_key=data.get("pub_key") and PublicKey.from_data(data["pub_key"]),
        )


@attr.s
class StdFee(JSONSerializable):

    gas: int = attr.ib(converter=int)
    amount: Coins = attr.ib(converter=Coins)

    @classmethod
    def from_data(cls, data: dict) -> StdFee:
        return cls(int(data["gas"]), Coins.from_data(data["amount"]))

    def to_data(self) -> dict:
        return {"gas": str(self.gas), "amount": self.amount.to_data()}

    @property
    def gas_prices(self) -> Coins:
        return self.amount.to_dec_coins().div(self.gas)


@attr.s
class StdSignMsg(JSONSerializable):

    chain_id: str = attr.ib()
    account_number: int = attr.ib(converter=int)
    sequence: int = attr.ib(converter=int)
    fee: StdFee = attr.ib()
    msgs: List[Msg] = attr.ib()
    memo: str = attr.ib()

    def to_stdtx(self) -> StdTx:
        return StdTx(self.msgs, self.fee, [], self.memo)

    def to_data(self) -> dict:
        return {
            "chain_id": self.chain_id,
            "account_number": str(self.account_number),
            "sequence": str(self.sequence),
            "fee": self.fee.to_data(),
            "msgs": [m.to_data() for m in self.msgs],
            "memo": self.memo,
        }

    @classmethod
    def from_data(cls, data: dict) -> StdSignMsg:
        return cls(
            data["chain_id"],
            int(data["account_number"]),
            int(data["sequence"]),
            StdFee.from_data(data["fee"]),
            [Msg.from_data(m) for m in data["msgs"]],
            data["memo"],
        )


@attr.s
class StdTx(JSONSerializable):

    msg: List[Msg] = attr.ib()
    fee: StdFee = attr.ib()
    signatures: List[StdSignature] = attr.ib()
    memo: str = attr.ib()

    def to_data(self) -> dict:
        return {
            "type": "core/StdTx",
            "value": {
                "msg": [m.to_data() for m in self.msg],
                "fee": self.fee.to_data(),
                "signatures": [s.to_data() for s in self.signatures],
                "memo": self.memo,
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> StdTx:
        data = data["value"]
        return cls(
            [Msg.from_data(m) for m in data["msg"]],
            StdFee.from_data(data["fee"]),
            [StdSignature.from_data(s) for s in data["signatures"]],
            data["memo"],
        )


def parse_events_by_type(event_data: List[dict]) -> Dict[str, Dict[str, List[str]]]:
    events: Dict[str, Dict[str, List[str]]] = {}
    for ev in event_data:
        for att in ev["attributes"]:
            if ev["type"] not in events:
                events[ev["type"]] = {}
            if att["key"] not in events[ev["type"]]:
                events[ev["type"]][att["key"]] = []
            events[ev["type"]][att["key"]].append(att["value"])
    return events


@attr.s
class TxLog(JSONSerializable):

    msg_index: int = attr.ib(converter=int)
    log: str = attr.ib()
    events: List[dict] = attr.ib()
    events_by_type: Dict[str, Dict[str, List[str]]] = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.events_by_type = parse_events_by_type(self.events)


def parse_tx_logs(logs) -> Optional[List[TxLog]]:
    return (
        [
            TxLog(msg_index=log["msg_index"], log=log["log"], events=log["events"])
            for log in logs
        ]
        if logs
        else None
    )


@attr.s
class TxInfo(JSONSerializable):

    height: int = attr.ib(converter=int)
    txhash: str = attr.ib()
    rawlog: str = attr.ib()
    logs: Optional[List[TxLog]] = attr.ib()
    gas_wanted: int = attr.ib(converter=int)
    gas_used: int = attr.ib(converter=int)
    tx: StdTx = attr.ib()
    timestamp: str = attr.ib()
    code: Optional[int] = attr.ib(default=None)
    codespace: Optional[str] = attr.ib(default=None)

    def to_data(self) -> dict:
        data = {
            "height": str(self.height),
            "txhash": self.txhash,
            "raw_log": self.rawlog,
            "logs": [log.to_data() for log in self.logs] if self.logs else None,
            "gas_wanted": str(self.gas_wanted),
            "gas_used": str(self.gas_used),
            "timestamp": self.timestamp,
            "tx": self.tx.to_data(),
            "code": self.code,
            "codespace": self.codespace,
        }

        if not self.logs:
            del data["logs"]

        if not self.code:
            del data["code"]

        if not self.codespace:
            del data["codespace"]

        return data

    @classmethod
    def from_data(cls, data: dict) -> TxInfo:
        return cls(
            data["height"],
            data["txhash"],
            data["raw_log"],
            parse_tx_logs(data["logs"]),
            data["gas_wanted"],
            data["gas_used"],
            StdTx.from_data(data["tx"]),
            data["timestamp"],
            data.get("code"),
            data.get("codespace"),
        )
