"""Auth mdoule message types."""

from __future__ import annotations

from terra_proto.cosmos.vesting.v1beta1 import (
    MsgDonateAllVestingTokens as MsgDonateAllVestingTokens_pb,
)

from terra_sdk.core import AccAddress, Coins
from terra_sdk.core.msg import Msg

__all__ = ["MsgDonateAllVestingTokens"]

import attr


@attr.s
class MsgDonateAllVestingTokens(Msg):
    """MsgDonateAllVestingTokens defines a message that enables donating all vesting.

    Args:
        from_address (AccAddress): address donating all vesting tokens.
    """

    type_amino = "cosmos-sdk/MsgDonateAllVestingTokens"
    type_url = "/cosmos.vesting.v1beta1.MsgDonateAllVestingTokens"
    prototype = MsgDonateAllVestingTokens_pb

    from_address: AccAddress = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "from_address": self.from_address,
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgDonateAllVestingTokens:
        return cls(
            from_address=data["from_address"],
        )

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "from_address": self.from_address,
        }

    @classmethod
    def from_proto(
        cls, proto: MsgDonateAllVestingTokens_pb
    ) -> MsgDonateAllVestingTokens:
        return cls(
            from_address=proto.from_address,
        )

    def to_proto(self) -> MsgDonateAllVestingTokens_pb:
        proto = MsgDonateAllVestingTokens_pb()
        proto.from_address = self.from_address
        return proto
