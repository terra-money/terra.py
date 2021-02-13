"""Gov module data types."""

from __future__ import annotations

import copy

import attr

from terra_sdk.core import Coins
from terra_sdk.util.base import BaseTerraData
from terra_sdk.util.json import JSONSerializable, dict_to_data

__all__ = ["Proposal", "Content"]


@attr.s
class Content(BaseTerraData):
    """Abstract proposal content type.

    .. note::
        This object is abstract, and not meant to be instantiated directly.
    """

    title: str = attr.ib()
    """"""
    description: str = attr.ib()
    """"""

    @staticmethod
    def from_data(data: dict) -> Content:
        from terra_sdk.util.parse_content import parse_content

        return parse_content(data)


@attr.s
class Proposal(JSONSerializable):
    """Contains information about a submitted proposal on the blockchain."""

    id: int = attr.ib(converter=int)
    """Proposal's ID."""

    content: Content = attr.ib()
    """Proposal contents."""

    proposal_status: str = attr.ib()
    """Status of proposal."""

    final_tally_result: dict = attr.ib()
    """Final tallied result of the proposal (after vote)."""

    submit_time: str = attr.ib()
    """Timestamp at which proposal was submitted."""

    deposit_end_time: str = attr.ib()
    """Time at which the deposit period ended, or will end."""

    total_deposit: Coins = attr.ib(converter=Coins)
    """Total amount deposited for proposal"""

    voting_start_time: str = attr.ib()
    """Time at which voting period started, or will start."""

    voting_end_time: str = attr.ib()
    """Time at which voting period ended, or will end."""

    def to_data(self) -> dict:
        d = copy.deepcopy(self.__dict__)
        d["id"] = str(d["id"])
        return dict_to_data(d)

    @classmethod
    def from_data(cls, data: dict) -> Proposal:
        return cls(
            id=data["id"],
            content=Content.from_data(data["content"]),
            proposal_status=data["proposal_status"],
            final_tally_result=data["final_tally_result"],
            submit_time=data["submit_time"],
            deposit_end_time=data["deposit_end_time"],
            total_deposit=Coins.from_data(data["total_deposit"]),
            voting_start_time=data["voting_start_time"],
            voting_end_time=data["voting_end_time"],
        )
