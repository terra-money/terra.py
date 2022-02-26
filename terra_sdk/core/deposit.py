from __future__ import annotations

import attr
from terra_proto.cosmos.gov.v1beta1 import Deposit as Deposit_pb

from terra_sdk.core import AccAddress
from terra_sdk.util.json import JSONSerializable

from .coins import Coins


@attr.s
class Deposit(JSONSerializable):
    proposal_id: int = attr.ib(converter=int)
    depositor: AccAddress = attr.ib()
    amount: Coins = attr.ib(converter=Coins)

    @classmethod
    def from_data(cls, data: dict) -> Deposit:
        return cls(
            proposal_id=data.get("proposal_id"),
            depositor=data.get("depositor"),
            amount=Coins.from_data(data.get("amount")),
        )

    @classmethod
    def from_proto(cls, proto: Deposit_pb) -> Deposit:
        return cls(
            proposal_id=proto.proposal_id,
            depositor=proto.depositor,
            amount=Coins.from_proto(proto.amount),
        )

    def to_proto(self) -> Deposit_pb:
        return Deposit_pb(
            proposal_id=self.proposal_id,
            depositor=self.depositor,
            amount=self.amount.to_proto(),
        )
