"""Params module governance proposal types."""

from __future__ import annotations

from typing import List

import attr

from terra_sdk.core.gov import Content

__all__ = ["ParameterChangeProposal"]


@attr.s
class ParameterChangeProposal(Content):
    """Proposal to alter the blockchain parameters. Changes would be effective
    as soon as the proposal is passed.

    Args:
        title: proposal title
        description: proposal description
        change (List[dict]): list of parameter changes
    """

    type = "params/ParameterChangeProposal"
    """"""

    title: str = attr.ib()
    description: str = attr.ib()
    changes: List[dict] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> ParameterChangeProposal:
        data = data["value"]
        return cls(
            title=data["title"],
            description=data["description"],
            changes=data["changes"],
        )
