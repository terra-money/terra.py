from __future__ import annotations

from dataclasses import dataclass


__all__ = ["TextProposal"]


@dataclass
class TextProposal(Content):

    type = "gov/TextProposal"


    title: str
    description: str

    @classmethod
    def from_data(cls, data: dict) -> TextProposal:
        data = data["value"]
        return cls(title=data["title"], description=data["description"])
