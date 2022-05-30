"""Slashing module messages types."""

from __future__ import annotations

import attr
from terra_proto.cosmos.slashing.v1beta1 import MsgUnjail as MsgUnjail_pb

from terra_sdk.core import ValAddress
from terra_sdk.core.msg import Msg

__all__ = ["MsgUnjail"]


@attr.s
class MsgUnjail(Msg):
    """Attempt to unjail a jailed validator (must be submitted by same validator).

    Args:
        address: validator address to unjail"""

    type_amino = "cosmos-sdk/MsgUnjail"
    """"""
    type_url = "/cosmos.slashing.v1beta1.MsgUnjail"
    """"""
    action = "unjail"
    """"""
    prototype = MsgUnjail_pb
    """"""

    address: ValAddress = attr.ib()

    def to_amino(self) -> dict:
        return {"type": self.type_amino, "value": {"address": self.address}}

    @classmethod
    def from_data(cls, data: dict) -> MsgUnjail:
        return cls(address=data["address"])

    def to_proto(self) -> MsgUnjail_pb:
        return MsgUnjail_pb(validator_addr=self.address)

    @classmethod
    def from_proto(cls, proto: MsgUnjail_pb) -> MsgUnjail:
        return cls(address=proto.address)
