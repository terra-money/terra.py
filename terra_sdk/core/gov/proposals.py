"""Gov module governance proposal types."""

from __future__ import annotations

from .data import Content

__all__ = ["TextProposal"]


class TextProposal(Content):
    """Generic proposal type with only title and description that does nothing if
    passed. Primarily used for assessing the community sentiment around the proposal.

    Args:
        title: proposal title
        description: proposal description
    """

    type = "gov/TextProposal"
    """"""

    @classmethod
    def from_data(cls, data: dict) -> TextProposal:
        data = data["value"]
        return cls(title=data["title"], description=data["description"])
