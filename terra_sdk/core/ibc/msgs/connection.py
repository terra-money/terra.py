"""ibc connection module message types."""

from __future__ import annotations

from typing import List

import attr
from betterproto.lib.google.protobuf import Any as Any_pb
from terra_proto.ibc.core.connection.v1 import (
    MsgConnectionOpenAck as MsgConnectionOpenAck_pb,
)
from terra_proto.ibc.core.connection.v1 import (
    MsgConnectionOpenConfirm as MsgConnectionOpenConfirm_pb,
)
from terra_proto.ibc.core.connection.v1 import (
    MsgConnectionOpenInit as MsgConnectionOpenInit_pb,
)
from terra_proto.ibc.core.connection.v1 import (
    MsgConnectionOpenTry as MsgConnectionOpenTry_pb,
)

from terra_sdk.core import AccAddress
from terra_sdk.core.ibc.data import Height
from terra_sdk.core.ibc.data.connection import Counterparty, Version
from terra_sdk.core.msg import Msg

__all__ = [
    "MsgConnectionOpenInit",
    "MsgConnectionOpenTry",
    "MsgConnectionOpenAck",
    "MsgConnectionOpenConfirm",
]


@attr.s
class MsgConnectionOpenInit(Msg):
    """
    MsgConnectionOpenInit defines the msg sent by an account on Chain A to initialize a connection with Chain B.
    """

    type_url = "/ibc.core.connection.v1.MsgConnectionOpenInit"
    """"""
    prototype = MsgConnectionOpenInit_pb
    """"""

    client_id: str = attr.ib()
    counterparty: Counterparty = attr.ib()
    version: Version = attr.ib()
    delay_period: int = attr.ib(converter=int)
    signer: AccAddress = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> MsgConnectionOpenInit:
        return cls(
            client_id=data["client_id"],
            counterparty=Counterparty.from_data(data["counterparty"]),
            version=Version.from_data(data["version"]),
            delay_period=data["delay_period"],
            signer=data["signer"],
        )

    def to_proto(self) -> MsgConnectionOpenInit_pb:
        return MsgConnectionOpenInit_pb(
            client_id=self.client_id,
            counterparty=self.counterparty.to_proto(),
            version=self.version.to_proto(),
            delay_period=self.delay_period,
            signer=self.signer,
        )

    @classmethod
    def from_proto(cls, proto: MsgConnectionOpenInit_pb) -> MsgConnectionOpenInit:
        return cls(
            client_id=proto.client_id,
            counterparty=Counterparty.from_proto(proto.counterparty),
            version=Version.from_proto(proto.version),
            delay_period=proto.delay_period,
            signer=proto.signer,
        )


@attr.s
class MsgConnectionOpenTry(Msg):
    """
    MsgConnectionOpenTry defines a msg sent by a Relayer to try to open a connection on Chain B.
    """

    type_url = "/ibc.core.connection.v1.MsgConnectionOpenTry"
    """"""
    prototype = MsgConnectionOpenTry_pb
    """"""

    client_id: str = attr.ib()
    previous_connection_id: str = attr.ib()
    client_state: dict = attr.ib()
    counterparty: Counterparty = attr.ib()
    delay_period: int = attr.ib(converter=int)
    counterparty_versions: List[Version] = attr.ib(converter=list)
    proof_height: Height = attr.ib()
    proof_init: bytes = attr.ib()
    proof_client: bytes = attr.ib()
    proof_consensus: bytes = attr.ib()
    consensus_height: Height = attr.ib()
    signer: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> MsgConnectionOpenTry:
        return cls(
            client_id=data["client_id"],
            previous_connection_id=data["previous_connection_id"],
            client_state=data["client_state"],
            counterparty=Counterparty.from_data(data["counterparty"]),
            delay_period=data["delay_period"],
            counterparty_versions=[
                Version.from_data(ver) for ver in data["counterparty_versions"]
            ],
            proof_height=Height.from_data(data["proof_height"]),
            proof_init=data["proof_init"],
            proof_client=data["proof_client"],
            proof_consensus=data["proof_consensus"],
            consensus_height=Height.from_data(data["consensus_height"]),
            signer=data["signer"],
        )

    def to_proto(self) -> MsgConnectionOpenTry_pb:
        return MsgConnectionOpenTry_pb(
            client_id=self.client_id,
            previous_connection_id=self.previous_connection_id,
            client_state=Any_pb().from_dict(self.client_state),
            counterparty=self.counterparty.to_proto(),
            delay_period=self.delay_period,
            counterparty_versions=[
                ver.to_proto() for ver in self.counterparty_versions
            ],
            proof_height=self.proof_height.to_proto(),
            proof_init=self.proof_init,
            proof_client=self.proof_client,
            proof_consensus=self.proof_consensus,
            consensus_height=self.consensus_height.to_proto(),
            signer=self.signer,
        )

    @classmethod
    def from_proto(cls, proto: MsgConnectionOpenTry_pb) -> MsgConnectionOpenTry:
        return cls(
            client_id=proto.client_id,
            previous_connection_id=proto.previous_connection_id,
            client_state=proto.client_state,
            counterparty=Counterparty.from_proto(proto.counterparty),
            delay_period=proto.delay_period,
            counterparty_versions=[
                Version.from_proto(ver) for ver in proto.counterparty_versions
            ],
            proof_height=Height.from_proto(proto.proof_height),
            proof_init=proto.proof_init,
            proof_client=proto.proof_client,
            proof_consensus=proto.proof_consensus,
            consensus_height=Height.from_proto(proto.consensus_height),
            signer=proto.signer,
        )


@attr.s
class MsgConnectionOpenAck(Msg):
    """
    MsgConnectionOpenAck defines a msg sent by a Relayer to Chain A to acknowledge the change of connection state to TRYOPEN on Chain B.
    """

    type_url = "/ibc.core.connection.v1.MsgConnectionOpenAck"
    """"""
    prototype = MsgConnectionOpenAck_pb
    """"""

    connection_id: str = attr.ib()
    counterparty_connection_id: str = attr.ib()
    version: Version = attr.ib()
    client_state: any = attr.ib()
    proof_height: Height = attr.ib()
    proof_try: bytes = attr.ib()
    proof_client: bytes = attr.ib()
    proof_consensus: bytes = attr.ib()
    consensus_height: Height = attr.ib()
    signer: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> MsgConnectionOpenAck:
        return cls(
            connection_id=data["connection_id"],
            counterparty_connection_id=data["counterparty_connection_id"],
            version=Version.from_data(data["version"]),
            client_state=data["client_state"],
            proof_height=Height.from_data(data["proof_height"]),
            proof_try=data["proof_try"],
            proof_client=data["proof_client"],
            proof_consensus=data["proof_consensus"],
            consensus_height=Height.from_data(data["consensus_height"]),
            signer=data["signer"],
        )

    def to_proto(self) -> MsgConnectionOpenAck_pb:
        return MsgConnectionOpenAck_pb(
            connection_id=self.connection_id,
            counterparty_connection_id=self.counterparty_connection_id,
            version=self.version.to_proto(),
            client_state=Any_pb().from_dict(self.client_state),
            proof_height=self.proof_height.to_proto(),
            proof_try=self.proof_try,
            proof_client=self.proof_client,
            proof_consensus=self.proof_consensus,
            consensus_height=self.consensus_height.to_proto(),
            signer=self.signer,
        )

    @classmethod
    def from_proto(cls, proto: MsgConnectionOpenAck_pb) -> MsgConnectionOpenAck:
        return cls(
            connection_id=proto.connection_id,
            counterparty_connection_id=proto.counterparty_connection_id,
            version=Version.from_proto(proto.version),
            client_state=Any_pb().parse(proto.client_state),
            proof_height=Height.from_proto(proto.proof_height),
            proof_try=proto.proof_try,
            proof_client=proto.proof_client,
            proof_consensus=proto.proof_consensus,
            consensus_height=Height.from_proto(proto.consensus_height),
            signer=proto.signer,
        )


@attr.s
class MsgConnectionOpenConfirm(Msg):
    """
    MsgConnectionOpenConfirm defines a msg sent by a Relayer to Chain B to acknowledge the change of connection state to OPEN on Chain A.
    """

    type_url = "/ibc.core.connection.v1.MsgConnectionOpenConfirm"
    """"""
    prototype = MsgConnectionOpenConfirm_pb
    """"""

    def to_amino(self):
        raise Exception("Amino not supported")

    connection_id: str = attr.ib()
    proof_ack: bytes = attr.ib()
    proof_height: Height = attr.ib()
    signer: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgConnectionOpenConfirm:
        return cls(
            connection_id=data["connection_id"],
            proof_ack=data["proof_ack"],
            proof_height=Height.from_data(data["proof_height"]),
            signer=data["signer"],
        )

    def to_proto(self) -> MsgConnectionOpenConfirm_pb:
        return MsgConnectionOpenConfirm_pb(
            connection_id=self.connection_id,
            proof_ack=self.proof_ack,
            proof_height=self.proof_height.to_proto(),
            signer=self.signer,
        )

    @classmethod
    def from_proto(cls, proto: MsgConnectionOpenConfirm_pb) -> MsgConnectionOpenConfirm:
        return cls(
            connection_id=proto.connection_id,
            proof_ack=proto.proof_ack,
            proof_height=Height.from_proto(proto.proof_height),
            signer=proto.signer,
        )
