from __future__ import annotations

from .data import Content

__all__ = ["TextProposal"]


class TextProposal(Content):

    type = "gov/TextProposal"

    @classmethod
    def from_data(cls, data: dict) -> TextProposal:
        data = data["value"]
        return cls(title=data["title"], description=data["description"])
