from __future__ import annotations

from dataclasses import dataclass


__all__ = ["TextProposal"]


@dataclass
class TextProposal(Content):

    type = "gov/TextProposal"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^gov/TextProposal\Z"),
        value=S.OBJECT(title=S.STRING, description=S.STRING),
    )

    title: str
    description: str

    @classmethod
    def from_data(cls, data: dict) -> TextProposal:
        data = data["value"]
        return cls(title=data["title"], description=data["description"])
