"""ibc connection module message types."""

from __future__ import annotations

import attr
from betterproto.lib.google.protobuf import Any as Any_pb
from terra_proto.ibc.core.client.v1 import MsgCreateClient as MsgCreateClient_pb
from terra_proto.ibc.core.client.v1 import (
    MsgSubmitMisbehaviour as MsgSubmitMisbehaviour_pb,
)
from terra_proto.ibc.core.client.v1 import MsgUpdateClient as MsgUpdateClient_pb
from terra_proto.ibc.core.client.v1 import MsgUpgradeClient as MsgUpgradeClient_pb

from terra_sdk.core.msg import Msg

__all__ = [
    "MsgCreateClient",
    "MsgUpdateClient",
    "MsgUpgradeClient",
    "MsgSubmitMisbehaviour",
]


@attr.s
class MsgCreateClient(Msg):
    """
    MsgCreateClientResponse defines the Msg/CreateClient response type.
    """

    type_url = "/ibc.core.client.v1.MsgCreateClient"
    """"""
    prototype = MsgCreateClient_pb
    """"""

    client_state: dict = attr.ib()
    consensus_state: dict = attr.ib()
    signer: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> MsgCreateClient:
        return cls(
            client_state=data["client_state"],
            consensus_state=data["consensus_state"],
            signer=data["signer"],
        )

    def to_proto(self) -> MsgCreateClient_pb:
        return MsgCreateClient_pb(
            client_state=Any_pb().from_dict(self.client_state),
            consensus_state=Any_pb().from_dict(self.consensus_state),
            signer=self.signer,
        )

    @classmethod
    def from_proto(cls, proto: MsgCreateClient_pb) -> MsgCreateClient:
        return cls(
            client_state=proto.client_state.to_dict(),
            consensus_state=proto.consensus_state.to_dict(),
            signer=proto.signer,
        )


@attr.s
class MsgUpdateClient(Msg):
    """
    MsgUpdateClient defines a sdk.Msg to update an IBC client state using the given header.
    """

    type_url = "/ibc.core.client.v1.MsgUpdateClient"
    """"""
    prototype = MsgUpdateClient_pb
    """"""

    client_id: str = attr.ib()
    header: dict = attr.ib()
    signer: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> MsgUpdateClient:
        return cls(
            client_id=data["client_id"], header=data["header"], signer=data["signer"]
        )

    def to_proto(self) -> MsgUpdateClient_pb:
        return MsgUpdateClient_pb(
            client_id=self.client_id,
            header=Any_pb().from_dict(self.header),
            signer=self.signer,
        )

    @classmethod
    def from_proto(cls, proto: MsgUpdateClient_pb) -> MsgUpdateClient:
        return cls(
            client_id=proto.client_id,
            header=proto.header.to_dict(),
            signer=proto.signer,
        )


@attr.s
class MsgUpgradeClient(Msg):
    """
    MsgUpgradeClient defines an sdk.Msg to upgrade an IBC client to a new client state
    """

    type_url = "/ibc.core.client.v1.MsgUpgradeClient"
    """"""
    prototype = MsgUpgradeClient_pb
    """"""

    client_id: str = attr.ib()
    client_state: dict = attr.ib()
    consensus_state: dict = attr.ib()
    proof_upgrade_client: bytes = attr.ib()
    proof_upgrade_consensus_state: bytes = attr.ib()
    signer: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> MsgUpgradeClient:
        return cls(
            client_id=data["client_id"],
            client_state=data["client_state"],
            consensus_state=data["consensus_state"],
            proof_upgrade_client=data["proof_upgrade_client"],
            proof_upgrade_consensus_state=data["proof_upgrade_consensus_state"],
            signer=data["signer"],
        )

    def to_proto(self) -> MsgUpgradeClient_pb:
        return MsgUpgradeClient_pb(
            client_id=self.client_id,
            client_state=Any_pb().from_dict(self.client_state),
            consensus_state=Any_pb().from_dict(self.consensus_state),
            proof_upgrade_client=self.proof_upgrade_client,
            proof_upgrade_consensus_state=self.proof_upgrade_consensus_state,
            signer=self.signer,
        )

    @classmethod
    def from_proto(cls, proto: MsgUpgradeClient_pb) -> MsgUpgradeClient:
        return cls(
            client_id=proto.client_id,
            client_state=proto.client_state.to_dict(),
            consensus_state=proto.consensus_state.to_dict(),
            proof_upgrade_client=proto.proof_upgrade_client,
            proof_upgrade_consensus_state=proto.proof_upgrade_consensus_state,
            signer=proto.signer,
        )


@attr.s
class MsgSubmitMisbehaviour(Msg):
    """
    MsgSubmitMisbehaviour defines a sdk.Msg type that submits Evidence for light client misbehaviour.
    """

    type_url = "/ibc.core.client.v1.MsgSubmitMisbehaviour"
    """"""
    prototype = MsgSubmitMisbehaviour_pb
    """"""

    client_id: str = attr.ib()
    misbehaviour: any = attr.ib()
    signer: str = attr.ib()

    def to_amino(self):
        raise Exception("Amino not supported")

    @classmethod
    def from_data(cls, data: dict) -> MsgSubmitMisbehaviour:
        return cls(
            client_id=data["client_id"],
            misbehaviour=data["misbehaviour"],
            signer=data["signer"],
        )

    def to_proto(self) -> MsgSubmitMisbehaviour_pb:
        return MsgSubmitMisbehaviour_pb(
            client_id=self.client_id,
            misbehaviour=Any_pb().from_dict(self.misbehaviour),
            signer=self.signer,
        )

    @classmethod
    def from_proto(cls, proto: MsgSubmitMisbehaviour_pb) -> MsgSubmitMisbehaviour:
        return cls(
            client_id=proto.client_id,
            misbehaviour=Any_pb().from_dict(proto.misbehaviour),
            signer=proto.signer,
        )
