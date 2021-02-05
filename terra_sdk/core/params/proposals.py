from __future__ import annotations

import attr

from terra_sdk.core.gov import Content

__all__ = ["ParameterChangeProposal"]


@attr.s
class ParameterChangeProposal(Content):

    type = "params/ParameterChangeProposal"

    title: str = attr.ib()
    description: str = attr.ib()
    changes: dict = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> ParameterChangeProposal:
        data = data["value"]
        return cls(
            title=data["title"],
            description=data["description"],
            changes=data["changes"],
        )
