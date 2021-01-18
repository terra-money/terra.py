"""Data objects related to building, signing, and broadcasting transactions."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import List, Optional



__all__ = [
    "StdFee",
    "StdSignature",
    "StdTx",
    "StdSignMsg",
    "TxInfo",
    "TxBroadcastResult",
]



@dataclass
class StdSignature(JsonSerializable, JsonDeserializable):

    __schema__ = S.OBJECT(signature=S.STRING, pub_key=PublicKey.__schema__)

    signature: str
    pub_key: PublicKey

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


@dataclass
class StdTx(JsonSerializable, JsonDeserializable):

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^core/StdTx\Z"),
        value=S.OBJECT(
            fee=StdFee.__schema__,
            msg=S.ARRAY(S.ANY(*(mt.__schema__ for mt in MSG_TYPES.values()))),
            signatures=S.ARRAY(StdSignature.__schema__),
            memo=S.STRING,
        ),
    )

    # NOTE: msg is not plural, and is NOT a typo. This may change later for consistency.
    fee: Optional[StdFee] = None
    msg: List[StdMsg] = field(default_factory=list)
    signatures: List[StdSignature] = field(default_factory=list)
    memo: str = ""

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


@dataclass
class StdSignMsg(JsonSerializable):

    # TODO: Add deserialization?

    chain_id: Optional[str] = None
    account_number: Optional[int] = None
    sequence: Optional[int] = None
    fee: Optional[StdFee] = None
    msgs: List[StdMsg] = field(default_factory=list)
    memo: str = ""

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


# Deprecated -- see MsgInfo
# @dataclass
# class TxLogEntry(JsonSerializable):
# __schema__ = S.OBJECT(
#     msg_index=S.INTEGER,
#     success=S.BOOLEAN,
#     log=S.STRING,
#     events=S.ARRAY(
#         S.OBJECT(
#             type=S.STRING,
#             attributes=S.ARRAY(S.OBJECT(key=S.STRING, value=S.STRING)),
#         )
#     ),
# )

# msg: StdMsg
# success: bool
# log: str
# events: dict

# def __post_init__(self):
#     try:
#         log = json.loads(self.log)
#         if type(log) == dict:
#             self.log = terra_sdkBox(log)
#     except:
#         log = None


@dataclass
class TxInfo(JsonSerializable, JsonDeserializable):
    """Holds data about a transaction that has been broadcasted and included in a block."""

    # TODO: Add Schema
    __schema__ = {}

    height: int
    txhash: str
    # logs: List[TxLogEntry] -- deprecated, log information uses MsgInfo right in msg now!
    gas_wanted: int
    gas_used: int
    timestamp: Timestamp

    # Merged with StdTx...
    # The rearrangement here from StdTx's arg list structure is
    # for better pretty-printing, and the fact that nobody will
    # be making TxInfo objects manually.
    fee: StdFee
    memo: str
    signatures: List[StdSignature]
    msg: List[MsgInfo]

    @property
    def tx(self):
        return StdTx(
            fee=self.fee, msg=self.msg, signatures=self.signatures, memo=self.memo
        )

    @property
    def msgs(self):
        # TODO: make the querying more powerful and extend to events
        """This is an alias because StdTx uses .msg whereas it makes more sense to use msgs."""
        return MsgInfosQuery(self.msg)

    @property
    def pretty_data(self):
        d = dict(self.__dict__)
        d.pop("msg")
        items = list(d.items())
        items.append(("msgs", self.msgs))
        return items

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

    @staticmethod
    def merge_logs(data: dict, tx: StdTx) -> List[MsgInfo]:
        """Joins logs and tx data together so that you can access log data straight
        from the MsgInfo."""
        temp_logs = data.get("logs")
        if temp_logs is None:
            logs = None
        else:
            logs = list()
            for i, l in enumerate(temp_logs):
                events = [Event.from_data(e) for e in l["events"]]
                logs.append(
                    MsgInfo(
                        msg=tx.msg[i],
                        success=l["success"],
                        log=l["log"],
                        events=EventsQuery(events),
                    ),
                )
        return logs


@dataclass
class TxBroadcastResult(JsonSerializable, JsonDeserializable):

    __schema__ = S.OBJECT(
        height=S.STRING_INTEGER,
        txhash=S.STRING,
        raw_log=S.STRING,
        logs=S.ARRAY(MsgInfo.__schema__),
        gas_wanted=S.STRING_INTEGER,
        gas_used=S.STRING_INTEGER,
        events=S.ARRAY({}),
    )

    height: int
    txhash: str
    raw_log: str
    # logs: list
    gas_wanted: int
    gas_used: int
    # events: list
    msgs: MsgInfosQuery

    @property
    def pretty_data(self):
        d = dict(self.__dict__)
        d.pop("raw_log")
        return d.items()

    @property
    def events(self):
        return self.msgs.events

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
