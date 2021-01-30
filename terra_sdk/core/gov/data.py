import attr
import copy

from terra_sdk.core import Coin, Coins
from terra_sdk.util.json import JSONSerializable, dict_to_data
from .content import Content

__all__ = ["Proposal"]


@attr.s
class Proposal(JSONSerializable):

    id: int = attr.ib(converter=int)
    content: Content = attr.ib()
    proposal_status: str = attr.ib()
    final_tally_result: dict = attr.ib()
    submit_time: str = attr.ib()
    deposit_end_time: str = attr.ib()
    total_deposit: Coins = attr.ib(converter=Coins)
    voting_start_time: str = attr.ib()
    voting_end_time: str = attr.ib()

    def to_data(self) -> dict:
        d = copy.deepcopy(self.__dict__)
        d["id"] = str(d["id"])
        return dict_to_data(d)

    @classmethod
    def from_data(cls, data: dict) -> Proposal:
        from terra_sdk.util.parse_content import parse_content

        return cls(
            id=data["id"],
            content=parse_content(data["content"]),
            proposal_status=data["proposal_status"],
            final_tally_result=data["final_tally_result"],
            submit_time=data["submit_time"],
            deposit_end_time=data["deposit_end_time"],
            total_deposit=Coins.from_data(data["total_deposit"]),
            voting_start_time=data["voting_start_time"],
            voting_end_time=data["voting_end_time"],
        )
