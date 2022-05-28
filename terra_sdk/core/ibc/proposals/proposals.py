from __future__ import annotations

import attr
from betterproto.lib.google.protobuf import Any as Any_pb
from terra_proto.ibc.core.client.v1 import (
    ClientUpdateProposal as ClientUpdateProposal_pb,
)

__all__ = ["ClientUpdateProposal"]

from terra_sdk.util.json import JSONSerializable


@attr.s
class ClientUpdateProposal(JSONSerializable):
    """Proposal that allows updating IBC clients. If it passes, the substitute
    client's latest consensus state is copied over to the subject client.

    """

    type_amino = "ibc/ClientUpdateProposal"
    """"""
    type_url = "/ibc.core.client.v1.ClientUpdateProposal"
    """"""
    prototype = ClientUpdateProposal_pb
    """"""

    title: str = attr.ib()
    description: str = attr.ib()
    subject_client_id: str = attr.ib()
    substitute_client_id: str = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "title": self.title,
                "description": self.description,
                "subject_client_id": self.subject_client_id,
                "substitute_client_id": self.substitute_client_id,
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> ClientUpdateProposal:
        return cls(
            title=data["title"],
            description=data["description"],
            subject_client_id=data["subject_client_id"],
            substitute_client_id=data["substitute_client_id"],
        )

    def to_proto(self) -> ClientUpdateProposal_pb:
        return ClientUpdateProposal_pb(
            title=self.title,
            description=self.description,
            subject_client_id=self.subject_client_id,
            substitute_client_id=self.substitute_client_id,
        )

    @classmethod
    def from_proto(cls, proto: ClientUpdateProposal_pb) -> ClientUpdateProposal:
        return cls(
            title=proto.title,
            description=proto.description,
            subject_client_id=proto.subject_client_id,
            substitute_client_id=proto.substitute_client_id,
        )

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))
