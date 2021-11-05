"""Gov module governance proposal types."""

from __future__ import annotations

from betterproto.lib.google.protobuf import Any as Any_pb
from terra_proto.cosmos.gov.v1beta1 import TextProposal as TextProposal_pb

from terra_sdk.util.json import JSONSerializable

__all__ = ["TextProposal"]


class TextProposal(JSONSerializable):
    """Generic proposal type with only title and description that does nothing if
    passed. Primarily used for assessing the community sentiment around the proposal.

    Args:
        title: proposal title
        description: proposal description
    """

    type_url = "/cosmos.gov.v1beta1.TextProposal"
    """"""

    @classmethod
    def from_data(cls, data: dict) -> TextProposal:
        return cls(title=data["title"], description=data["description"])

    def to_proto(self) -> TextProposal_pb:
        return TextProposal_pb(title=self.title, description=self.description)

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))
