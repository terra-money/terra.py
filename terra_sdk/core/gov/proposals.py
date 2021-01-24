from __future__ import annotations

import attr

__all__ = ["TextProposal"]


@attr.s
class TextProposal(Content):

    type = "gov/TextProposal"

    title: str = attr.ib()
    description: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> TextProposal:
        data = data["value"]
        return cls(title=data["title"], description=data["description"])
