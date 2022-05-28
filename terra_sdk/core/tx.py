"""Data objects pertaining to building, signing, and parsing Transactions."""

from __future__ import annotations

import base64
import json
from typing import Dict, List, Optional

import attr
from betterproto.lib.google.protobuf import Any
from terra_proto.cosmos.base.abci.v1beta1 import AbciMessageLog as AbciMessageLog_pb
from terra_proto.cosmos.base.abci.v1beta1 import Attribute as Attribute_pb
from terra_proto.cosmos.base.abci.v1beta1 import StringEvent as StringEvent_pb
from terra_proto.cosmos.base.abci.v1beta1 import TxResponse as TxResponse_pb
from terra_proto.cosmos.tx.signing.v1beta1 import SignMode as SignMode_pb
from terra_proto.cosmos.tx.v1beta1 import AuthInfo as AuthInfo_pb
from terra_proto.cosmos.tx.v1beta1 import SignerInfo as SignerInfo_pb
from terra_proto.cosmos.tx.v1beta1 import Tx as Tx_pb
from terra_proto.cosmos.tx.v1beta1 import TxBody as TxBody_pb

from terra_sdk.core.compact_bit_array import CompactBitArray
from terra_sdk.core.fee import Fee
from terra_sdk.core.mode_info import ModeInfo, ModeInfoMulti, ModeInfoSingle
from terra_sdk.core.msg import Msg
from terra_sdk.core.public_key import (
    LegacyAminoMultisigPublicKey,
    PublicKey,
    SimplePublicKey,
)
from terra_sdk.core.signature_v2 import SignatureV2
from terra_sdk.util.json import JSONSerializable

__all__ = [
    "SignMode",
    "AuthInfo",
    "Tx",
    "TxBody",
    "TxLog",
    "TxInfo",
    "parse_tx_logs",
    "SignerInfo",
    "SignerData",
]

# just alias
from terra_sdk.util.parse_msg import parse_proto

SignMode = SignMode_pb


@attr.s
class SignerData:
    sequence: int = attr.ib(converter=int)
    public_key: Optional[PublicKey] = attr.ib(default=None)


@attr.s
class Tx(JSONSerializable):
    """Data structure for a transaction which can be broadcasted.

    Args:
        body (TxBody): the processable content of the transaction
        auth_info (AuthInfo): the authorization related content of the transaction
        signatures (List[bytes]): signatures is a list of signatures that matches the length and order of body and auth_info
    """

    body: TxBody = attr.ib()
    auth_info: AuthInfo = attr.ib()
    signatures: List[bytes] = attr.ib(converter=list)

    def to_data(self) -> dict:
        return {
            "body": self.body.to_data(),
            "auth_info": self.auth_info.to_data(),
            "signatures": [
                base64.b64encode(sig).decode("ascii") for sig in self.signatures
            ],
        }

    def to_proto(self) -> Tx_pb:
        return Tx_pb(
            body=self.body.to_proto(),
            auth_info=self.auth_info.to_proto(),
            signatures=self.signatures,
        )

    @classmethod
    def from_data(cls, data: dict) -> Tx:
        return cls(
            TxBody.from_data(data["body"]),
            AuthInfo.from_data(data["auth_info"]),
            [base64.b64decode(sig) for sig in data["signatures"]],
        )

    @classmethod
    def from_proto(cls, proto: Tx_pb) -> Tx:
        return cls(
            TxBody.from_proto(proto.body),
            AuthInfo.from_proto(proto.auth_info),
            proto.signatures,
        )

    @classmethod
    def from_bytes(cls, txb: bytes) -> Tx:
        proto = Tx_pb().parse(txb)
        c = cls.from_proto(proto)
        return c

    def append_empty_signatures(self, signers: List[SignerData]):
        for signer in signers:
            if signer.public_key is not None:
                if isinstance(signer.public_key, LegacyAminoMultisigPublicKey):
                    signer_info = SignerInfo(
                        public_key=signer.public_key,
                        sequence=signer.sequence,
                        mode_info=ModeInfo(
                            multi=ModeInfoMulti(
                                CompactBitArray.from_bits(
                                    len(signer.public_key.public_keys)
                                ),
                                [],
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

    def clear_signature(self):
        self.signatures.clear()
        self.auth_info.signer_infos.clear()

    def append_signatures(self, signatures: List[SignatureV2]):
        for sig in signatures:
            mode_info, sig_bytes = sig.data.to_mode_info_and_signature()
            self.signatures.append(sig_bytes)
            # self.signatures.append(base64.b64decode(sig_bytes))
            self.auth_info.signer_infos.append(
                SignerInfo(sig.public_key, mode_info, sig.sequence)
            )


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
    timeout_height: int = attr.ib(
        default=0, converter=int
    )  # TxBody_pb.timeout_height is int

    def to_data(self) -> dict:
        return {
            "messages": [m.to_data() for m in self.messages],
            "memo": self.memo,
            "timeout_height": self.timeout_height,
        }

    def to_proto(self) -> TxBody_pb:
        return TxBody_pb(
            messages=[m.pack_any() for m in self.messages],
            memo=self.memo,
            timeout_height=self.timeout_height,
        )

    @classmethod
    def from_data(cls, data: dict) -> TxBody:
        return cls(
            [Msg.from_data(m) for m in data["messages"]],
            data["memo"],
            data["timeout_height"] if data["timeout_height"] else 0,
        )

    @classmethod
    def from_proto(cls, proto: TxBody_pb) -> TxBody:
        return cls(
            [Msg.unpack_any(m) for m in proto.messages],
            proto.memo,
            proto.timeout_height,
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
    def from_proto(cls, proto: AuthInfo_pb) -> AuthInfo:
        return cls(
            [SignerInfo.from_proto(m) for m in proto.signer_infos],
            Fee.from_proto(proto.fee),
        )


@attr.s
class SignerInfo(JSONSerializable):
    """SignerInfo
    Args:
       public_key (PublicKey)
       mode_info (ModeInfo)
       sequence (int)
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
            public_key=PublicKey.unpack_any(proto.public_key),
            mode_info=ModeInfo.from_proto(proto.mode_info),
            sequence=proto.sequence,
        )


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
        events = [json.loads(event) for event in tx_log.events]
        return cls(msg_index=tx_log.msg_index, log=tx_log.log, events=events)

    def to_proto(self) -> AbciMessageLog_pb:
        str_events = []
        for event in self.events:
            str_events.append(json.dumps(event))
        return AbciMessageLog_pb(
            msg_index=self.msg_index, log=self.log, events=str_events
        )


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

        return data

    @classmethod
    def from_data(cls, data: dict) -> TxInfo:
        return cls(
            data.get("height"),
            data.get("txhash"),
            data.get("raw_log"),
            parse_tx_logs(data.get("logs")),
            data.get("gas_wanted"),
            data.get("gas_used"),
            Tx.from_data(data.get("tx")),
            data.get("timestamp"),
            data.get("code"),
            data.get("codespace"),
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
            height=proto.height,
            txhash=proto.txhash,
            rawlog=proto.raw_log,
            logs=parse_tx_logs_proto(proto.logs),
            gas_wanted=proto.gas_wanted,
            gas_used=proto.gas_used,
            timestamp=proto.timestamp,
            tx=Tx.from_proto(proto.tx),
            code=proto.code,
            codespace=proto.codespace,
        )
