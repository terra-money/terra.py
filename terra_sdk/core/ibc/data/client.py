"""ibc client module data objects."""
from __future__ import annotations

from typing import List

import attr
from betterproto.lib.google.protobuf import Any as Any_pb
from terra_proto.ibc.core.client.v1 import (
    ClientConsensusStates as ClientConsensusStates_pb,
)
from terra_proto.ibc.core.client.v1 import (
    ConsensusStateWithHeight as ConsensusStateWithHeight_pb,
)
from terra_proto.ibc.core.client.v1 import Height as Height_pb
from terra_proto.ibc.core.client.v1 import (
    IdentifiedClientState as IdentifiedClientState_pb,
)
from terra_proto.ibc.core.client.v1 import Params as Params_pb

from terra_sdk.util.json import JSONSerializable

__all__ = [
    "Height",
    "IdentifiedClientState",
    "ConsensusStateWithHeight",
    "ClientConsensusStates",
    "Params",
]


@attr.s
class Height(JSONSerializable):
    revision_number: int = attr.ib(converter=int)
    revision_height: int = attr.ib(converter=int)

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> Height:
        return cls(
            revision_number=data["revision_number"],
            revision_height=data["revision_height"],
        )

    def to_proto(self) -> Height_pb:
        return Height_pb(
            revision_number=self.revision_number, revision_height=self.revision_height
        )

    @classmethod
    def from_proto(cls, proto: Height_pb) -> Height:
        return cls(
            revision_number=proto.revision_number,
            revision_height=proto.revision_height,
        )


@attr.s
class IdentifiedClientState(JSONSerializable):
    """
    IdentifiedClientState defines a client state with an additional client identifier field.
    """

    client_id: str = attr.ib()
    client_state: dict = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> IdentifiedClientState:
        return cls(
            client_id=data["client_id"],
            client_state=Any_pb().from_dict(data["client_state"]),
        )

    def to_proto(self) -> IdentifiedClientState_pb:
        return IdentifiedClientState_pb(
            client_id=self.client_id,
            client_state=Any_pb().from_dict(self.client_state),
        )

    @classmethod
    def from_proto(cls, proto: IdentifiedClientState_pb) -> IdentifiedClientState:
        return cls(
            client_id=proto.client_id, client_state=proto.client_state.to_dict()
        )


@attr.s
class ConsensusStateWithHeight(JSONSerializable):
    """
    ConsensusStateWithHeight defines a consensus state with an additional height field.
    """

    height: Height = attr.ib()
    consensus_state: dict = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> ConsensusStateWithHeight:
        return cls(
            height=data["height"],
            consensus_state=Any_pb().from_dict(data["consensus_state"]),
        )

    def to_proto(self) -> ConsensusStateWithHeight_pb:
        return ConsensusStateWithHeight_pb(
            height=self.height.to_proto(),
            consensus_state=Any_pb().from_dict(self.consensus_state),
        )

    @classmethod
    def from_proto(cls, proto: ConsensusStateWithHeight_pb) -> ConsensusStateWithHeight:
        return cls(
            height=Height.from_proto(proto.height),
            consensus_state=proto.consensus_state.to_dict(),
        )


@attr.s
class ClientConsensusStates(JSONSerializable):
    """
    ClientConsensusStates defines all the stored consensus states for a given client.
    """

    client_id: str = attr.ib()
    consensus_states: List[ConsensusStateWithHeight] = attr.ib(converter=list)

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> ClientConsensusStates:
        return cls(
            client_id=data["client_id"],
            consensus_states=[
                ConsensusStateWithHeight.from_data(state)
                for state in data["consensus_states"]
            ],
        )

    def to_proto(self) -> ClientConsensusStates_pb:
        return ClientConsensusStates_pb(
            client_id=self.client_id,
            consensus_states=[state.to_proto() for state in self.consensus_states],
        )

    @classmethod
    def from_proto(cls, proto: ClientConsensusStates_pb) -> ClientConsensusStates:
        return cls(
            client_id=proto.client_id,
            consensus_states=[
                ConsensusStateWithHeight.from_proto(state)
                for state in proto.consensus_states
            ],
        )


@attr.s
class Params(JSONSerializable):
    """
    Params defines the set of IBC light client parameters.
    """

    allowed_clients: List[str] = attr.ib(converter=list)

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> Params:
        return cls(allowed_clients=data["allowed_clients"])

    def to_proto(self) -> Params_pb:
        return Params_pb(allowed_clients=self.allowed_clients)

    @classmethod
    def from_proto(cls, proto: Params_pb) -> Params:
        return cls(allowed_clients=proto.allowed_clients)
