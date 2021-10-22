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

    type_url = "/cosmos.params.v1beta1.ParameterChangeProposal"
    """"""

    title: str = attr.ib()
    description: str = attr.ib()
    changes: List[dict] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> ParameterChangeProposal:
        return cls(
            title=data["title"],
            description=data["description"],
            changes=data["changes"],
        )
