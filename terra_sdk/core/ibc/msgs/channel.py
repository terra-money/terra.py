"""ibc connection module message types."""

from __future__ import annotations

import attr
from terra_proto.ibc.core.channel.v1 import MsgAcknowledgement as MsgAcknowledgement_pb
from terra_proto.ibc.core.channel.v1 import (
    MsgChannelCloseConfirm as MsgChannelCloseConfirm_pb,
)
from terra_proto.ibc.core.channel.v1 import (
    MsgChannelCloseInit as MsgChannelCloseInit_pb,
)
from terra_proto.ibc.core.channel.v1 import MsgChannelOpenAck as MsgChannelOpenAck_pb
from terra_proto.ibc.core.channel.v1 import (
    MsgChannelOpenConfirm as MsgChannelOpenConfirm_pb,
)
from terra_proto.ibc.core.channel.v1 import MsgChannelOpenInit as MsgChannelOpenInit_pb
from terra_proto.ibc.core.channel.v1 import MsgChannelOpenTry as MsgChannelOpenTry_pb
from terra_proto.ibc.core.channel.v1 import MsgRecvPacket as MsgRecvPacket_pb
from terra_proto.ibc.core.channel.v1 import MsgTimeout as MsgTimeout_pb

from terra_sdk.core.ibc.data.channel import Channel, Packet
from terra_sdk.core.ibc.data.client import Height
from terra_sdk.core.msg import Msg

# TODO: support MsgTimeoutClose
__all__ = [
    "MsgChannelOpenInit",
    "MsgChannelOpenTry",
    "MsgChannelOpenAck",
    "MsgChannelOpenConfirm",
    "MsgChannelCloseInit",
    "MsgChannelCloseConfirm",
    "MsgRecvPacket",
    "MsgTimeout",
    "MsgAcknowledgement",
]


@attr.s
class MsgChannelOpenInit(Msg):
    """
    MsgChannelOpenInit defines an sdk.Msg to initialize a channel handshake. It
    is called by a relayer on Chain A.
    """

    type_url = "/ibc.core.channel.v1.MsgChannelOpenInit"
    """"""
    prototype = MsgChannelOpenInit_pb
    """"""

    port_id: str = attr.ib()
    channel: Channel = attr.ib()
    signer: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> MsgChannelOpenInit:
        return cls(
            port_id=data["port_id"],
            channel=Channel.from_data(data["port_id"]),
            signer=data["signer"],
        )

    def to_proto(self) -> MsgChannelOpenInit_pb:
        return MsgChannelOpenInit_pb(
            port_id=self.port_id, channel=self.channel.to_proto(), signer=self.signer
        )

    @classmethod
    def from_proto(cls, proto: MsgChannelOpenInit_pb) -> MsgChannelOpenInit:
        return cls(
            port_id=proto.port_id,
            channel=Channel.from_proto(proto.channel),
            signer=proto.signer,
        )


@attr.s
class MsgChannelOpenTry(Msg):
    """
    MsgChannelOpenInit defines a msg sent by a Relayer to try to open a channel
    on Chain B.
    """

    type_url = "/ibc.core.channel.v1.MsgChannelOpenTry"
    """"""
    prototype = MsgChannelOpenTry_pb
    """"""

    port_id: str = attr.ib()
    previous_channel_id: str = attr.ib()
    channel: Channel = attr.ib()
    counterparty_version: str = attr.ib()
    proof_init: bytes = attr.ib()
    proof_height: Height = attr.ib()
    signer: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> MsgChannelOpenTry:
        return cls(
            port_id=data["port_id"],
            previous_channel_id=data["previous_channel_id"],
            channel=Channel.from_data(data["channel"]),
            counterparty_version=data["counterparty_version"],
            proof_init=data["proof_init"],
            proof_height=Height.from_data(data["proof_height"]),
            signer=data["signer"],
        )

    def to_proto(self) -> MsgChannelOpenTry_pb:
        return MsgChannelOpenTry_pb(
            port_id=self.port_id,
            previous_channel_id=self.previous_channel_id,
            channel=self.channel.to_proto(),
            counterparty_version=self.counterparty_version,
            proof_init=self.proof_init,
            proof_height=self.proof_height.to_proto(),
            signer=self.signer,
        )

    @classmethod
    def from_proto(cls, proto: MsgChannelOpenTry_pb) -> MsgChannelOpenTry:
        return cls(
            port_id=proto.port_id,
            previous_channel_id=proto.previous_channel_id,
            channel=Channel.from_proto(proto.channel),
            counterparty_version=proto.counterparty_version,
            proof_init=proto.proof_init,
            proof_height=Height.from_proto(proto.proof_height),
            signer=proto.signer,
        )


class MsgChannelOpenAck(Msg):
    """
    MsgChannelOpenAck defines a msg sent by a Relayer to Chain A to acknowledge
    the change of channel state to TRYOPEN on Chain B.
    """

    type_url = "/ibc.core.channel.v1.MsgChannelOpenAck"
    """"""
    prototype = MsgChannelOpenAck_pb
    """"""

    port_id: str = attr.ib()
    channel_id: str = attr.ib()
    counterparty_channel_id: str = attr.ib()
    counterparty_version: str = attr.ib()
    proof_try: bytes = attr.ib()
    proof_height: Height = attr.ib()
    signer: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> MsgChannelOpenAck:
        return cls(
            port_id=data["port_id"],
            channel_id=data["channel_id"],
            counterparty_channel_id=data["counterparty_channel_id"],
            counterparty_version=data["counterparty_version"],
            proof_try=data["proof_try"],
            proof_height=Height.from_data(data["proof_height"]),
            signer=data["signer"],
        )

    def to_proto(self) -> MsgChannelOpenAck_pb:
        return MsgChannelOpenAck_pb(
            port_id=self.port_id,
            channel_id=self.channel_id,
            counterparty_channel_id=self.counterparty_channel_id,
            counterparty_version=self.counterparty_version,
            proof_try=self.proof_try,
            proof_height=self.proof_height.to_proto(),
            signer=self.signer,
        )

    @classmethod
    def from_proto(cls, proto: MsgChannelOpenAck) -> MsgChannelOpenAck:
        return cls(
            port_id=proto.port_id,
            channel_id=proto.channel_id,
            counterparty_channel_id=proto.counterparty_channel_id,
            counterparty_version=proto.counterparty_version,
            proof_try=proto.proof_try,
            proof_height=Height.from_proto(proto.proof_height),
            signer=proto.signer,
        )


@attr.s
class MsgChannelOpenConfirm(Msg):
    """
    MsgChannelOpenConfirm defines a msg sent by a Relayer to Chain B to
    acknowledge the change of channel state to OPEN on Chain A.
    """

    type_url = "/ibc.core.channel.v1.MsgChannelOpenConfirm"
    """"""
    prototype = MsgChannelOpenConfirm_pb
    """"""

    port_id: str = attr.ib()
    channel_id: str = attr.ib()
    proof_ack: bytes = attr.ib()
    proof_height: Height = attr.ib()
    signer: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> MsgChannelOpenConfirm:
        return cls(
            port_id=data["port_id"],
            channel_id=data["channel_id"],
            proof_ack=data["proof_ack"],
            proof_height=Height.from_data(data["proof_height"]),
            signer=data["signer"],
        )

    def to_proto(self) -> MsgChannelOpenConfirm_pb:
        return MsgChannelOpenConfirm_pb(
            port_id=self.port_id,
            channel_id=self.channel_id,
            proof_ack=self.proof_ack,
            proof_height=self.proof_height.to_proto(),
            signer=self.signer,
        )

    @classmethod
    def from_proto(cls, proto: MsgChannelOpenConfirm_pb) -> MsgChannelOpenConfirm:
        return cls(
            port_id=proto.port_id,
            channel_id=proto.channel_id,
            proof_ack=proto.proof_ack,
            proof_height=Height.from_proto(proto.proof_height),
            signer=proto.signer,
        )


@attr.s
class MsgChannelCloseInit(Msg):
    """ """

    type_url = "/ibc.core.channel.v1.MsgChannelCloseInit"
    """"""
    prototype = MsgChannelCloseInit_pb
    """"""

    port_id: str = attr.ib()
    channel_id: str = attr.ib()
    signer: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> MsgChannelCloseInit:
        return cls(
            port_id=data["port_id"],
            channel_id=data["channel_id"],
            signer=data["signer"],
        )

    def to_proto(self) -> MsgChannelCloseInit_pb:
        return MsgChannelCloseInit_pb(
            port_id=self.port_id, channel_id=self.channel_id, signer=self.signer
        )

    @classmethod
    def from_proto(cls, proto: MsgChannelOpenInit_pb) -> MsgChannelCloseInit:
        return cls(
            port_id=proto.port_id, channel_id=proto.channel_id, signer=proto.signer
        )


@attr.s
class MsgChannelCloseConfirm(Msg):
    """
    MsgChannelCloseConfirm defines a msg sent by a Relayer to Chain B to
    acknowledge the change of channel state to CLOSED on Chain A.
    """

    type_url = "/ibc.core.channel.v1.MsgChannelCloseConfirm"
    """"""
    prototype = MsgChannelCloseConfirm_pb
    """"""

    port_id: str = attr.ib()
    channel_id: str = attr.ib()
    proof_init: bytes = attr.ib()
    proof_height: Height = attr.ib()
    signer: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> MsgChannelCloseConfirm:
        return cls(
            port_id=data["port_id"],
            channel_id=data["channel_id"],
            proof_init=data["proof_init"],
            proof_height=Height.from_data(data["proof_height"]),
            signer=data["signer"],
        )

    def to_proto(self) -> MsgChannelCloseConfirm_pb:
        return MsgChannelCloseConfirm_pb(
            port_id=self.port_id,
            channel_id=self.channel_id,
            proof_init=self.proof_init,
            proof_height=self.proof_height.to_proto(),
            signer=self.signer,
        )

    @classmethod
    def from_proto(cls, proto: MsgChannelCloseConfirm_pb) -> MsgChannelCloseConfirm:
        return cls(
            port_id=proto.port_id,
            channel_id=proto.channel_id,
            proof_init=proto.proof_init,
            proof_height=Height.from_proto(proto.proof_height),
            signer=proto.signer,
        )


@attr.s
class MsgRecvPacket(Msg):
    """
    MsgRecvPacket receives incoming IBC packet
    """

    type_url = "/ibc.core.channel.v1.MsgRecvPacket"
    """"""
    prototype = MsgRecvPacket_pb
    """"""

    packet: Packet = attr.ib()
    proof_commitment: bytes = attr.ib()
    proof_height: Height = attr.ib()
    signer: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> MsgRecvPacket:
        return cls(
            packet=Packet.from_data(data["packet"]),
            proof_commitment=data["proof_commitment"],
            proof_height=Height.from_data(data["proof_height"]),
            signer=data["signer"],
        )

    def to_proto(self) -> MsgRecvPacket_pb:
        return MsgRecvPacket_pb(
            packet=self.packet.to_proto(),
            proof_commitment=self.proof_commitment,
            proof_height=self.proof_height.to_proto(),
            signer=self.signer,
        )

    @classmethod
    def from_proto(cls, proto: MsgRecvPacket_pb) -> MsgRecvPacket:
        return cls(
            packet=Packet.from_proto(proto.packet),
            proof_commitment=proto.proof_commitment,
            proof_height=Height.from_proto(proto.proof_height),
            signer=proto.signer,
        )


@attr.s
class MsgTimeout(Msg):
    """
    MsgTimeout receives timed-out packet
    """

    type_url = "/ibc.core.channel.v1.MsgTimeout"
    """"""
    prototype = MsgTimeout_pb
    """"""

    packet: Packet = attr.ib()
    proof_unreceived: bytes = attr.ib()
    proof_height: Height = attr.ib()
    next_sequence_recv: int = attr.ib(converter=int)
    signer: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> MsgTimeout:
        return cls(
            packet=Packet.from_data(data["packet"]),
            proof_unreceived=data["proof_unreceived"],
            proof_height=Height.from_data(data["proof_height"]),
            next_sequence_recv=data["next_sequence_recv"],
            signer=data["signer"],
        )

    def to_proto(self) -> MsgTimeout_pb:
        return MsgTimeout_pb(
            packet=self.packet.to_proto(),
            proof_unreceived=self.proof_unreceived,
            proof_height=self.proof_height.to_proto(),
            next_sequence_recv=self.next_sequence_recv,
            signer=self.signer,
        )

    @classmethod
    def from_proto(cls, proto: MsgTimeout_pb) -> MsgTimeout:
        return cls(
            packet=Packet.from_proto(proto.packet),
            proof_unreceived=proto.proof_unreceived,
            proof_height=Height.from_proto(proto.proof_height),
            next_sequence_recv=proto.next_sequence_recv,
            signer=proto.signer,
        )


@attr.s
class MsgAcknowledgement(Msg):
    """
    MsgAcknowledgement receives incoming IBC acknowledgement
    """

    type_url = "/ibc.core.channel.v1.MsgAcknowledgement"
    """"""
    prototype = MsgAcknowledgement_pb
    """"""

    packet: Packet = attr.ib()
    acknowledgement: bytes = attr.ib()
    proof_acked: bytes = attr.ib()
    proof_height: Height = attr.ib()
    signer: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> MsgAcknowledgement:
        return cls(
            packet=Packet.from_data(data["packet"]),
            acknowledgement=data["acknowledgement"],
            proof_acked=data["proof_acked"],
            proof_height=Height.from_data(data["proof_height"]),
            signer=data["signer"],
        )

    def to_proto(self) -> MsgAcknowledgement_pb:
        return MsgAcknowledgement_pb(
            packet=self.packet.to_proto(),
            acknowledgement=self.acknowledgement,
            proof_acked=self.proof_acked,
            proof_height=self.proof_height.to_proto(),
            signer=self.signer,
        )

    @classmethod
    def from_proto(cls, proto: MsgAcknowledgement_pb) -> MsgAcknowledgement:
        return cls(
            packet=Packet.from_proto(proto.packet),
            acknowledgement=proto.acknowledgement,
            proof_acked=proto.proof_acked,
            proof_height=Height.from_proto(proto.proof_height),
            signer=proto.signer,
        )
