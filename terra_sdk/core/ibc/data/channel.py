"""ibc channel module data objects."""
from __future__ import annotations

from typing import List

import attr
from terra_proto.ibc.core.channel.v1 import Channel as Channel_pb
from terra_proto.ibc.core.channel.v1 import Counterparty as Counterparty_pb
from terra_proto.ibc.core.channel.v1 import Order
from terra_proto.ibc.core.channel.v1 import Packet as Packet_pb
from terra_proto.ibc.core.channel.v1 import State

from terra_sdk.core.ibc.data.client import Height
from terra_sdk.util.json import JSONSerializable

__all__ = ["Counterparty", "Channel", "Order", "State", "Packet"]


@attr.s
class Counterparty(JSONSerializable):
    """
    Counterparty defines a channel end counterparty
    """

    port_id: str = attr.ib()
    channel_id: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> Counterparty:
        return cls(
            port_id=data["port_id"],
            channel_id=data["channel_id"],
        )

    def to_proto(self) -> Counterparty_pb:
        return Counterparty_pb(port_id=self.port_id, channel_id=self.channel_id)

    @classmethod
    def from_proto(cls, proto: Counterparty_pb) -> Counterparty:
        return cls(
            port_id=proto.port_id,
            channel_id=proto.channel_id,
        )


@attr.s
class Channel(JSONSerializable):
    """
    Channel defines pipeline for exactly-once packet delivery between specific
    modules on separate blockchains, which has at least one end capable of
    sending packets and one end capable of receiving packets.
    """

    state: State = attr.ib(converter=int)
    ordering: Order = attr.ib(converter=int)
    counterparty: Counterparty = attr.ib()
    connection_hops: List[str] = attr.ib(converter=list)
    version: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> Channel:
        return cls(
            state=data["state"],
            ordering=data["ordering"],
            counterparty=Counterparty.from_data(data["counterparty"]),
            connection_hops=data["connection_hops"],
            version=data["version"],
        )

    def to_proto(self) -> Channel_pb:
        return Channel_pb(
            state=self.state,
            ordering=self.ordering,
            counterparty=self.counterparty.to_proto(),
            connection_hops=self.connection_hops,
            version=self.version,
        )

    @classmethod
    def from_proto(cls, proto: Channel_pb) -> Channel:
        return cls(
            state=proto.state,
            ordering=proto.ordering,
            counterparty=Counterparty.from_proto(proto.counterparty),
            connection_hops=proto.connection_hops,
            version=proto.version,
        )


@attr.s
class Packet(JSONSerializable):
    """
    Packet defines a type that carries data across different chains through IBC
    """

    sequence: int = attr.ib(converter=int)
    source_port: str = attr.ib()
    source_channel: str = attr.ib()
    destination_port: str = attr.ib()
    destination_channel: str = attr.ib()
    data: bytes = attr.ib()
    timeout_height: Height = attr.ib()
    timeout_timestamp: int = attr.ib(converter=int)

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> Packet:
        return cls(
            sequence=data["sequence"],
            source_port=data["source_port"],
            source_channel=data["source_channel"],
            destination_port=data["destination_port"],
            destination_channel=data["destination_channel"],
            data=data["data"],
            timeout_height=Height.from_data(data["timeout_height"]),
            timeout_timestamp=data["timeout_timestamp"],
        )

    def to_proto(self) -> Packet_pb:
        return Packet_pb(
            sequence=self.sequence,
            source_port=self.source_port,
            source_channel=self.source_channel,
            destination_port=self.destination_port,
            destination_channel=self.destination_channel,
            data=self.data,
            timeout_height=self.timeout_height.to_proto(),
            timeout_timestamp=self.timeout_timestamp,
        )

    @classmethod
    def from_proto(cls, proto: Packet_pb) -> Packet:
        return cls(
            sequence=proto.sequence,
            source_port=proto.source_port,
            source_channel=proto.source_channel,
            destination_port=proto.destination_port,
            destination_channel=proto.destination_channel,
            data=proto.data,
            timeout_height=Height.from_proto(proto.timeout_height),
            timeout_timestamp=proto.timeout_timestamp,
        )
