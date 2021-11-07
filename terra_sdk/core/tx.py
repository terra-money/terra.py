"""Data objects pertaining to building, signing, and parsing Transactions."""

from __future__ import annotations

import base64
import math
from typing import Dict, List, Optional

import attr
from betterproto.lib.google.protobuf import Any as Any_pb
from terra_proto.cosmos.base.abci.v1beta1 import AbciMessageLog as AbciMessageLog_pb
from terra_proto.cosmos.base.abci.v1beta1 import Attribute as Attribute_pb
from terra_proto.cosmos.base.abci.v1beta1 import StringEvent as StringEvent_pb
from terra_proto.cosmos.base.abci.v1beta1 import TxResponse as TxResponse_pb
from terra_proto.cosmos.crypto.multisig.v1beta1 import (
    CompactBitArray as CompactBitArray_pb,
)
from terra_proto.cosmos.tx.signing.v1beta1 import SignMode as SignMode_pb
from terra_proto.cosmos.tx.v1beta1 import AuthInfo as AuthInfo_pb
from terra_proto.cosmos.tx.v1beta1 import ModeInfo as ModeInfo_pb
from terra_proto.cosmos.tx.v1beta1 import ModeInfoMulti as ModeInfoMulti_pb
from terra_proto.cosmos.tx.v1beta1 import ModeInfoSingle as ModeInfoSingle_pb
from terra_proto.cosmos.tx.v1beta1 import SignerInfo as SignerInfo_pb
from terra_proto.cosmos.tx.v1beta1 import Tx as Tx_pb
from terra_proto.cosmos.tx.v1beta1 import TxBody as TxBody_pb

from terra_sdk.core.fee import Fee
from terra_sdk.core.msg import Msg
from terra_sdk.core.public_key import LegacyAminoPubKey, PublicKey, SimplePublicKey
from terra_sdk.util.json import JSONSerializable

__all__ = [
    "SignMode",
    "AuthInfo",
    "Tx",
    "TxBody",
    "TxLog",
    "TxInfo",
    "parse_tx_logs",
    "ModeInfo",
    "ModeInfoSingle",
    "ModeInfoMulti",
    "SignerInfo",
    "SignerData",
    "CompactBitArray",
]

# just alias
SignMode = SignMode_pb


@attr.s
class SignerData:
    sequence: int = attr.ib(converter=int)
    public_key: Optional[PublicKey] = attr.ib(default=None)


@attr.s
class Tx(JSONSerializable):
    """Data structure for a transaction which can be broadcasted.

    Args:
        body: the processable content of the transaction
        auth_info: the authorization related content of the transaction
        signatures: signatures is a list of signatures that matches the length and order of body and auth_info
    """

    body: TxBody = attr.ib()
    auth_info: AuthInfo = attr.ib()
    signatures: List[bytes] = attr.ib(converter=list)

    def to_data(self) -> dict:
        return {
            "body": self.body.to_data(),
            "auth_info": self.auth_info.to_data(),
            "signatures": [base64.b64encode(sig).decode() for sig in self.signatures],
        }

    def to_proto(self) -> Tx_pb:
        proto = Tx_pb()
        proto.body = self.body.to_proto()
        proto.auth_info = self.auth_info.to_proto()
        proto.signatures = [sig for sig in self.signatures]
        return proto

    @classmethod
    def from_data(cls, data: dict) -> Tx:
        return cls(
            TxBody.from_data(data["body"]),
            AuthInfo.from_data(data["auth_info"]),
            data["signatures"],
        )

    @classmethod
    def from_proto(cls, proto: Tx_pb) -> Tx:
        return cls(
            TxBody.from_proto(proto["body"]),
            AuthInfo.from_proto(proto["auth_info"]),
            proto["signatures"],
        )

    def append_empty_signatures(self, signers: List[SignerData]):
        for signer in signers:
            if signer.public_key is not None:
                if isinstance(signer.public_key, LegacyAminoPubKey):
                    signer_info = SignerInfo(
                        public_key=signer.public_key,
                        sequence=signer.sequence,
                        mode_info=ModeInfo(
                            ModeInfoMulti(
                                CompactBitArray.from_bits(
                                    len(signer.public_key.public_keys)
                                )
                            )
                        ),
                    )
                else:
                    signer_info = SignerInfo(
                        public_key=signer.public_key,
                        sequence=signer.sequence,
                        mode_info=ModeInfo(
                            ModeInfoSingle(mode=SignMode.SIGN_MODE_DIRECT)
                        ),
                    )
            else:
                signer_info = SignerInfo(
                    public_key=SimplePublicKey(""),
                    sequence=signer.sequence,
                    mode_info=ModeInfo(ModeInfoSingle(mode=SignMode.SIGN_MODE_DIRECT)),
                )
            self.auth_info.signer_infos.append(signer_info)
            self.signatures.append(b" ")


@attr.s
class TxBody(JSONSerializable):
    """Body of a transaction.

    Args:
        messages: list of messages to include in transaction
        memo: transaction memo
        timeout_height:
    """

    messages: List[Msg] = attr.ib()
    memo: Optional[str] = attr.ib(default="")
    timeout_height: Optional[int] = attr.ib(default=None)

    def to_data(self) -> dict:
        return {
            "messages": [m.to_data() for m in self.messages],
            "memo": self.memo if self.memo else "",
            "timeout_height": self.timeout_height if self.timeout_height else 0,
        }

    def to_proto(self) -> TxBody_pb:
        return TxBody_pb(
            messages=[m.pack_any() for m in self.messages],
            memo=self.memo or "",
            timeout_height=self.timeout_height,
        )

    @classmethod
    def from_data(cls, data: dict) -> TxBody:
        return cls(
            [Msg.from_data(m) for m in data["messages"]],
            data["memo"],
            data["timeout_height"],
        )

    @classmethod
    def from_proto(cls, proto: TxBody_pb) -> TxBody:
        return cls(
            [Msg.unpack_any(m) for m in proto["messages"]],
            proto["memo"],
            proto["timeout_height"],
        )


@attr.s
class AuthInfo(JSONSerializable):
    """AuthInfo
    Args:
        signer_infos: information of the signers
        fee: Fee
    """

    signer_infos: List[SignerInfo] = attr.ib(converter=list)
    fee: Fee = attr.ib()

    def to_dict(self, casing, include_default_values) -> dict:
        return self.to_proto().to_dict(casing, include_default_values)

    def to_data(self) -> dict:
        return {
            "signer_infos": [si.to_data() for si in self.signer_infos],
            "fee": self.fee.to_data(),
        }

    def to_proto(self) -> AuthInfo_pb:
        return AuthInfo_pb(
            signer_infos=[signer.to_proto() for signer in self.signer_infos],
            fee=self.fee.to_proto(),
        )

    @classmethod
    def from_data(cls, data: dict) -> AuthInfo:
        return cls(
            [SignerInfo.from_data(m) for m in data["signer_infos"]],
            Fee.from_data(data["fee"]),
        )

    @classmethod
    def from_proto(cls, proto: TxBody_pb) -> TxBody:
        return cls(
            [SignerInfo.from_proto(m) for m in proto["signer_infos"]],
            Fee.from_proto(proto["fee"]),
        )


@attr.s
class SignerInfo(JSONSerializable):
    """SignerInfo
    Args:
       public_key:
       sequence:
       mode_info:
    """

    public_key: PublicKey = attr.ib()
    mode_info: ModeInfo = attr.ib()
    sequence: int = attr.ib(converter=int)

    def to_data(self) -> dict:
        return {
            "public_key": self.public_key.to_data(),
            "mode_info": self.mode_info.to_data(),
            "sequence": self.sequence,
        }

    def to_proto(self) -> SignerInfo_pb:
        return SignerInfo_pb(
            public_key=self.public_key.pack_any(),
            mode_info=self.mode_info.to_proto(),
            sequence=self.sequence,
        )

    @classmethod
    def from_data(cls, data: dict) -> SignerInfo:
        return cls(
            public_key=PublicKey.from_data(data["public_key"]),
            mode_info=ModeInfo.from_data(data["mode_info"]),
            sequence=data["sequence"],
        )

    @classmethod
    def from_proto(cls, proto: SignerInfo_pb) -> SignerInfo:
        return cls(
            public_key=PublicKey.from_proto(proto["public_key"]),
            mode_info=ModeInfo.from_proto(proto["mode_info"]),
            sequence=proto["sequence"],
        )


@attr.s
class ModeInfo(JSONSerializable):

    single: Optional[ModeInfoSingle] = attr.ib(default=None)
    multi: Optional[ModeInfoMulti] = attr.ib(default=None)

    def to_data(self) -> dict:
        return {
            "single": self.single.to_data() if self.single else None,
            "multi": self.multi.todata() if self.multi else None,
        }

    @classmethod
    def from_data(cls, data: dict) -> ModeInfo:
        return cls(
            ModeInfoSingle.from_data(data.get("single"))
            if data.get("single")
            else None,
            ModeInfoMulti.from_data(data.get("multi")) if data.get("multi") else None,
        )

    def to_proto(self) -> ModeInfo_pb:
        if self.single:
            return ModeInfo_pb(single=self.single.to_proto())
        else:
            return ModeInfo_pb(multi=self.multi.to_proto())

    @classmethod
    def from_proto(cls, proto: ModeInfo_pb) -> ModeInfo:
        if proto["single"]:
            return ModeInfoSingle.from_proto(proto["single"])
        else:
            return ModeInfoMulti.from_proto(proto["multi"])


@attr.s
class ModeInfoSingle(JSONSerializable):
    mode: SignMode = attr.ib()

    def to_data(self) -> dict:
        {"mode": self.mode}

    @classmethod
    def from_data(cls, data: dict) -> ModeInfoSingle:
        return cls(data["mode"])

    def to_proto(self) -> Any_pb:
        return ModeInfoSingle_pb(mode=self.mode)

    @classmethod
    def from_proto(cls, proto: ModeInfoSingle_pb) -> ModeInfoSingle:
        mode = SignMode.from_string(proto["mode"])
        return cls(mode=mode)


@attr.s
class ModeInfoMulti(JSONSerializable):
    bitarray: CompactBitArray = attr.ib()
    mode_infos: List[ModeInfo] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> ModeInfoMulti:
        return cls(data["bitarray"], data["mode_infos"])

    def to_proto(self) -> ModeInfoMulti_pb:
        proto = ModeInfoMulti_pb()
        proto.bitarray = self.bitarray.to_proto()
        proto.mode_infos = [mi.to_proto() for mi in self.mode_infos]
        return proto

    @classmethod
    def from_proto(cls, proto: ModeInfoMulti_pb) -> ModeInfoMulti:
        return cls(
            CompactBitArray.from_proto(proto["bitarray"]),
            ModeInfo_pb.from_proto(proto["mode_infos"]),
        )


@attr.s
class CompactBitArray(JSONSerializable):
    extra_bits_stored: int = attr.ib(converter=int)
    elems: bytes = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> CompactBitArray:
        return cls(data["extra_bits_stored"], data["elems"])

    @classmethod
    def from_proto(cls, proto: CompactBitArray_pb) -> CompactBitArray:
        return cls(proto["extra_bits_stored"], proto["elems"])

    def to_proto(self) -> CompactBitArray_pb:
        return CompactBitArray_pb(
            extra_bits_stored=self.extra_bits_stored, elems=self.elems
        )

    @classmethod
    def from_bits(cls, bits: int) -> CompactBitArray:
        if bits <= 0:
            raise ValueError("CompactBitArray bits must be bigger than 0")

        num_elems = (bits + 7) / 8
        if num_elems <= 0 or num_elems > (math.pow(2, 32) - 1):
            raise ValueError("CompactBitArray overflow")

        return CompactBitArray(bits % 8, bytes(num_elems))

    def count(self) -> int:
        if self.extra_bits_stored == 0:
            return len(self.elems) * 8
        return (len(self.elems) - 1) * 8 + self.extra_bits_stored

    def get_index(self, i: int) -> bool:
        if i < 0 or i >= self.count():
            return False
        return self.elems[(i >> 3)] & ((1 << (7 - (i % 8))) > 0)

    def set_index(self, i: int, v: bool) -> bool:
        if i < 0 or i >= self.count():
            return False
        if v:  # True
            self.elems[i >> 3] |= 1 << (7 - (i % 8))
        else:  # False
            self.elems[i >> 3] &= ~(1 << (7 - (i % 8)))
        return True

    def num_true_bits_before(self, index: int) -> int:
        def count_one_bits(n: int):
            return len("{0:b}".format(n).split("0").join(""))

        ones_count = 0
        max = self.count()
        if index > max:
            index = max

        elem = 0
        while True:
            if elem * 8 + 7 >= index:
                ones_count += count_one_bits(self.elems[elem] >> (7 - (index % 8) + 1))
                return ones_count
            ones_count += count_one_bits(self.elems[elem])


def parse_events_by_type(event_data: List[dict]) -> Dict[str, Dict[str, List[str]]]:
    events: Dict[str, Dict[str, List[str]]] = {}
    for ev in event_data:
        for att in ev["attributes"]:
            if ev["type"] not in events:
                events[ev["type"]] = {}
            if att["key"] not in events[ev["type"]]:
                events[ev["type"]][att["key"]] = []
            events[ev["type"]][att["key"]].append(att.get("value"))
    return events


@attr.s
class TxLog(JSONSerializable):
    """Object containing the events of a transaction that is automatically generated when
    :class:`TxInfo` or :class:`BlockTxBroadcastResult` objects are read."""

    msg_index: int = attr.ib(converter=int)
    """Number of the message inside the transaction that it was included in."""

    log: str = attr.ib()
    """This field may be populated with details of the message's error, if any."""

    events: List[dict] = attr.ib()
    """Raw event log data"""

    events_by_type: Dict[str, Dict[str, List[str]]] = attr.ib(init=False)
    """Event log data, re-indexed by event type name and attribute type.

    For instance, the event type may be: ``store_code`` and an attribute key could be
    ``code_id``.

    >>> logs[0].events_by_type["<event-type>"]["<attribute-key>"]
    ['<attribute-value>', '<attribute-value2>']
    """

    def __attrs_post_init__(self):
        self.events_by_type = parse_events_by_type(self.events)

    @classmethod
    def from_proto(cls, tx_log: AbciMessageLog_pb) -> TxLog:
        events = [event for event in tx_log["events"]]
        return cls(msg_index=tx_log["msg_index"], log=tx_log["log"], events=events)


@attr.s
class Attribute(JSONSerializable):
    key: str = attr.ib()
    value: str = attr.ib()

    def to_proto(self) -> Attribute_pb:
        proto = Attribute_pb()
        proto.key = self.key
        proto.value = self.value
        return proto

    @classmethod
    def from_proto(cls, attrib: Attribute_pb) -> Attribute:
        return cls(key=attrib["key"], value=attrib["value"])


@attr.s
class StringEvent(JSONSerializable):

    type: str = attr.ib()
    attributes = attr.ib()

    def to_proto(self) -> StringEvent_pb:
        return StringEvent_pb(type=self.type, attributes=self.attributes)

    @classmethod
    def from_proto(cls, str_event: StringEvent_pb) -> StringEvent:
        return cls(type=str_event["type"], attributes=str_event["attributes"])


def parse_tx_logs(logs) -> Optional[List[TxLog]]:
    return (
        [
            TxLog(msg_index=i, log=log.get("log"), events=log.get("events"))
            for i, log in enumerate(logs)
        ]
        if logs
        else None
    )


def parse_tx_logs_proto(logs: List[AbciMessageLog_pb]) -> Optional[List[TxLog]]:
    return [TxLog.from_proto(log) for log in logs] if logs else None


@attr.s
class TxInfo(JSONSerializable):
    """Holds information pertaining to a transaction which has been included in a block
    on the blockchain.

    .. note::
        Users are not expected to create this object directly. It is returned by
        :meth:`TxAPI.tx_info()<terra_sdk.client.lcd.api.tx.TxAPI.tx_info>`
    """

    height: int = attr.ib(converter=int)
    """Block height at which transaction was included."""

    txhash: str = attr.ib()
    """Transaction hash."""

    rawlog: str = attr.ib()
    """Event log information as a raw JSON-string."""

    logs: Optional[List[TxLog]] = attr.ib()
    """Event log information."""

    gas_wanted: int = attr.ib(converter=int)
    """Gas requested by transaction."""

    gas_used: int = attr.ib(converter=int)
    """Actual gas amount used."""

    tx: Tx = attr.ib()
    """Transaction object."""

    timestamp: str = attr.ib()
    """Time at which transaction was included."""

    code: Optional[int] = attr.ib(default=None)
    """If this field is not ``None``, the transaction failed at ``DeliverTx`` stage."""

    codespace: Optional[str] = attr.ib(default=None)
    """Error subspace (used alongside ``code``)."""

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
        tx = data["tx"]
        resp = data["tx_response"]
        return cls(
            resp["height"],
            resp["txhash"],
            resp["raw_log"],
            parse_tx_logs(resp.get("logs")),
            resp["gas_wanted"],
            resp["gas_used"],
            Tx.from_data(tx),
            resp["timestamp"],
            resp.get("code"),
            resp.get("codespace"),
        )

    def to_proto(self) -> TxResponse_pb:
        proto = TxResponse_pb()
        proto.height = self.height
        proto.txhash = self.txhash
        proto.raw_log = self.rawlog
        proto.logs = [log.to_proto() for log in self.logs] if self.logs else None
        proto.gas_wanted = self.gas_wanted
        proto.gas_used = self.gas_used
        proto.timestamp = self.timestamp
        proto.tx = self.tx.to_proto()
        proto.code = self.code
        proto.codespace = self.codespace
        return proto

    @classmethod
    def from_proto(cls, proto: TxResponse_pb) -> TxInfo:
        return cls(
            height=proto["height"],
            txhash=proto["txhash"],
            rawlog=proto["raw_log"],
            logs=parse_tx_logs_proto(proto["logs"]),
            gas_wanted=proto["gas_wanted"],
            gas_used=proto["gas_used"],
            timestamp=proto["timestamp"],
            tx=Tx.from_proto(proto["tx"]),
            code=proto["code"],
            codespace=proto["codespace"],
        )
