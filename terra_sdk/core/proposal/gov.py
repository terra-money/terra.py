from __future__ import annotations

from dataclasses import dataclass

from terra_sdk.core.proposal import Content
from terra_sdk.util.validation import Schemas as S

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
