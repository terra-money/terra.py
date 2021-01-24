import attr

from .coin import Coin
from .coins import Coins

__all__ = ["Proposal"]


@attr.s
class Proposal:

    id: int = attr.ib()
    content: Content = attr.ib()
    proposal_status: str = attr.ib()
    final_tally_result: dict = attr.ib()
    submit_time: Date = attr.ib()
    deposit_end_time: Date = attr.ib()
    total_deposit: Coins = attr.ib()
    voting_start_time: Date = attr.ib()
    voting_end_time: Date = attr.ib()

    def to_data(self) -> dict:
        d = terra_sdkBox(self.__dict__)
        d.id = str(d.id)
        for x in d.final_tally_result:
            d.final_tally_result[x] = d.final_tally_result[x].amount
        return d

    @classmethod
    def from_data(cls, data: dict) -> Proposal:
        final_tally_result = data["final_tally_result"]
        for key in final_tally_result:
            final_tally_result[key] = Coin(uLuna, int(final_tally_result[key]))
        p_type = PROPOSAL_TYPES[data["content"]["type"]]
        content = p_type.from_data(data["content"])
        return cls(
            id=int(data["id"]),
            content=Content.from_data(data["content"]),
            proposal_status=ProposalStatus(data["proposal_status"]),
            final_tally_result=terra_sdkBox(final_tally_result),
            submit_time=Timestamp.from_data(data["submit_time"]),
            deposit_end_time=Timestamp.from_data(data["deposit_end_time"]),
            total_deposit=Coins.from_data(data["total_deposit"]),
            voting_start_time=Timestamp.from_data(data["voting_start_time"]),
            voting_end_time=Timestamp.from_data(data["voting_end_time"]),
        )
