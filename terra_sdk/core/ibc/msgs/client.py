"""ibc connection module message types."""

from __future__ import annotations

from typing import Optional, Any, List

import attr
from terra_proto.ibc.core.client.v1 import (
    MsgCreateClient as MsgCreateClient_pb,
    MsgUpdateClient as MsgUpdateClient_pb,
    MsgUpgradeClient as MsgUpgradeClient_pb,
    MsgSubmitMisbehaviour as MsgSubmitMisbehaviour_pb
)
from betterproto.lib.google.protobuf import Any as Any_pb

from terra_sdk.core.msg import Msg

__all__ = ["MsgCreateClient", "MsgUpdateClient", "MsgUpgradeClient", "MsgSubmitMisbehaviour"]


@attr.s
class MsgCreateClient(Msg):
    """
    MsgCreateClientResponse defines the Msg/CreateClient response type.
    """

    type_url = "/ibc.core.client.v1.MsgCreateClient"
    """"""

    client_state: Any_pb = attr.ib()
    consensus_state: Any_pb = attr.ib()
    signer: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> MsgCreateClient:
        return cls(
            client_state=Any_pb.FromString(data["client_state"]),
            consensus_state=Any_pb.FromString(data["consensus_state"]),
            signer=data["signer"]
        )

    def to_proto(self) -> MsgCreateClient_pb:
        return MsgCreateClient_pb(
            client_state=self.client_state,
            consensus_state=self.consensus_state,
            signer=self.signer
        )


@attr.s
class MsgUpdateClient(Msg):
    """
    MsgUpdateClient defines an sdk.Msg to update a IBC client state using the given header.
    """

    type_url = "/ibc.core.client.v1.MsgUpdateClient"
    """"""

    client_id: str = attr.ib()
    header: Any_pb = attr.ib()
    signer: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> MsgUpdateClient:
        return cls(
            client_id=data["client_id"],
            header=Any_pb.FromString(data["header"]),
            signer=data["signer"]
        )

    def to_proto(self) -> MsgUpdateClient_pb:
        return MsgUpdateClient_pb(
            client_id=self.client_id,
            header=self.header,
            signer=self.signer
        )



@attr.s
class MsgUpgradeClient(Msg):
    """
    MsgUpgradeClient defines an sdk.Msg to upgrade an IBC client to a new client state
    """

    type_url = "/ibc.core.client.v1.MsgUpgradeClient"
    """"""

    client_id: str = attr.ib()
    client_state: Any_pb = attr.ib()
    consensus_state: Any_pb = attr.ib()
    proof_upgrade_client: bytes = attr.ib()
    proof_upgrade_consensus_state: bytes = attr.ib()
    signer: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> MsgUpgradeClient:
        return cls(
            client_id=data["client_id"],
            client_state=Any_pb.FromString(data["client_state"]),
            consensus_state=Any_pb.FromString(data["consensus_state"]),
            proof_upgrade_client=data["proof_upgrade_client"],
            proof_upgrade_consensus_state=data["proof_upgrade_consensus_state"],
            signer=data["signer"]
        )

    def to_proto(self) -> MsgUpgradeClient_pb:
        return MsgUpgradeClient_pb(
            client_id=self.client_id,
            client_state=self.client_state,
            consensus_state=self.consensus_state,
            proof_upgrade_client=self.proof_upgrade_client,
            proof_upgrade_consensus_state=self.proof_upgrade_consensus_state,
            signer=self.signer
        )


@attr.s
class MsgSubmitMisbehaviour(Msg):
    """
    MsgSubmitMisbehaviour defines an sdk.Msg type that submits Evidence for light client misbehaviour.
    """

    type_url = "/ibc.core.client.v1.MsgSubmitMisbehaviour"
    """"""

    client_id: str = attr.ib()
    misbehaviour: Any_pb = attr.ib()
    signer: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> MsgSubmitMisbehaviour:
        return cls(
            client_id=data["client_id"],
            misbehaviour=Any_pb.FromString(data["misbehaviour"]),
            signer=data["signer"]
        )

    def to_proto(self) -> MsgSubmitMisbehaviour_pb:
        return MsgSubmitMisbehaviour_pb(
            client_id=self.client_id,
            misbehaviour=self.misbehaviour,
            signer=self.signer
        )
