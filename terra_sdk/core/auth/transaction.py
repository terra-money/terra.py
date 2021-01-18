"""Data objects related to building, signing, and broadcasting transactions."""

from __future__ import annotations

import json
import attr

__all__ = [
    "StdFee",
    "StdSignature",
    "StdTx",
    "StdSignMsg",
    "TxInfo",
    "TxBroadcastResult",
]


@attr.s
class StdSignature(JsonSerializable, JsonDeserializable):

    signature: str = attr.ib()
    pub_key: PublicKey = attr.ib()

    def __str__(self) -> str:
        return self.signature

    @classmethod
    def from_data(cls, data: dict) -> StdSignature:
        if data is None:
            return None
        return cls(
            signature=data.get("signature"),
            pub_key=PublicKey.from_data(data.get("pub_key")),
        )


@attr.s
class StdTx(JsonSerializable, JsonDeserializable):

    # NOTE: msg is not plural, and is NOT a typo. This may change later for consistency.
    fee: Optional[StdFee] = attr.ib()
    msg: List[StdMsg] = attr.ib()
    signatures: List[StdSignature] = attr.ib()
    memo: str = attr.ib()

    def to_data(self) -> dict:
        return {
            "type": "core/StdTx",
            "value": dict(self.__dict__),
        }

    @classmethod
    def from_data(cls, data: dict) -> StdTx:
        data = data["value"]
        fee = StdFee.from_data(data["fee"])
        # deserialize the messages
        msg = []
        for m in data["msg"]:
            msg_type = MSG_TYPES[m["type"]]
            msg.append(msg_type.from_data(m))
        signatures = [StdSignature.from_data(s) for s in data["signatures"]]
        return cls(fee=fee, msg=msg, signatures=signatures, memo=data["memo"])


@attr.s
class StdSignMsg(JsonSerializable):

    chain_id: Optional[str] = attr.ib()
    account_number: Optional[int] = attr.ib()
    sequence: Optional[int] = attr.ib()
    fee: Optional[StdFee] = attr.ib()
    msgs: List[StdMsg] = attr.ib()
    memo: str = attr.ib()

    def to_tx(self) -> StdTx:
        """Get the associated `StdTx` value of the sign message, with the
        `signatures` attribute set to `None`.
        """
        return StdTx(fee=self.fee, msg=self.msgs, signatures=None, memo=self.memo)

    def to_data(self) -> dict:
        d = dict(self.__dict__)
        d["account_number"] = str(self.account_number)
        d["sequence"] = str(self.sequence)
        return d



@attr.s
class TxInfo(JsonSerializable, JsonDeserializable):
    """Holds data about a transaction that has been broadcasted and included in a block."""

    height: int = attr.ib()
    txhash: str = attr.ib()
    gas_wanted: int = attr.ib()
    gas_used: int = attr.ib()
    timestamp: Timestamp = attr.ib()

    # TODO: fix Vv
    # Merged with StdTx...
    # The rearrangement here from StdTx's arg list structure is
    # for better pretty-printing, and the fact that nobody will
    # be making TxInfo objects manually.
    fee: StdFee
    memo: str
    signatures: List[StdSignature]
    msg: List[MsgInfo]


    def to_data(self) -> dict:
        logs = []
        for i, msginfo in enumerate(self.msg):  # treat as a log
            logs.append(
                {
                    "msg_index": i,
                    "success": msginfo.success,
                    "log": json.dumps(msginfo.log),
                    "events": [event for l in msginfo.events.values() for event in l],
                }
            )
            print(logs)

        print(logs)
        return {
            "height": self.height,
            "txhash": self.txhash,
            "logs": logs,
            "gas_wanted": self.gas_wanted,
            "gas_used": self.gas_used,
            "timestamp": self.timestamp,
            "tx": self.tx,
        }

    @classmethod
    def from_data(cls, data: dict) -> TxInfo:
        tx = data.get("tx") and StdTx.from_data(data["tx"])
        # need to merge tx.msg and logs to get something useful!
        # schema(log) = {msg_index: int, success: bool, log: str, events: event[]}
        # schema(event) = {attributes: [{key: ..., value: ...}], type: str}
        logs = TxInfo.merge_logs(data, tx)
        return cls(
            height=data.get("height") and int(data["height"]),
            txhash=data.get("txhash"),
            # logs=None,
            gas_wanted=data.get("gas_wanted") and int(data["gas_wanted"]),
            gas_used=data.get("gas_used") and int(data["gas_used"]),
            timestamp=data.get("timestamp") and Timestamp.from_data(data["timestamp"]),
            fee=tx.fee,
            msg=logs,
            signatures=tx.signatures,
            memo=tx.memo,
        )



@attr.s
class TxBroadcastResult(JsonSerializable, JsonDeserializable):

    height: int         = attr.ib()
    txhash: str         = attr.ib()
    raw_log: str        = attr.ib()
    # logs: list        = attr.ib()
    gas_wanted: int     = attr.ib()
    gas_used: int       = attr.ib()
    # events: list      = attr.ib()
    msgs: MsgInfosQuery = attr.ib()

    @classmethod
    def from_data(cls, data: dict, tx) -> TxBroadcastResult:
        logs = TxInfo.merge_logs(data, tx)
        if logs:
            logs = MsgInfosQuery(logs)
        return cls(
            height=data.get("height") and int(data["height"]),
            txhash=data.get("txhash"),
            raw_log=data.get("raw_log"),
            gas_wanted=data.get("gas_wanted") and int(data["gas_wanted"]),
            gas_used=data.get("gas_used") and int(data["gas_used"]),
            # events=data.get("events"),
            msgs=logs,
        )
