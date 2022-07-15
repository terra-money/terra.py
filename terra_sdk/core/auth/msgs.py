"""Auth mdoule message types."""

from __future__ import annotations

from betterproto.lib.google.protobuf import Any as Any_pb
from terra_proto.cosmos.vesting.v1beta1 import (
    MsgCreateVestingAccount as MsgCreateVestingAccount_pb,
    MsgCreatePeriodicVestingAccount as MsgCreatePeriodicVestingAccount_pb,
    MsgDonateAllVestingTokens as MsgDonateAllVestingTokens_pb,
)
from terra_sdk.core.auth.data.periodic_vesting_account import Period

from typing import List
from terra_sdk.core import AccAddress, Coins
from terra_sdk.core.msg import Msg

__all__ =["MsgCreateVestingAccount", "MsgCreatePeriodicVestingAccount", "MsgDonateAllVestingTokens"]

import attr

@attr.s
class MsgCreateVestingAccount(Msg):
    """MsgCreateVestingAccount defines a message that enables creating a vesting.
    
    Args:
        from_address 
        to_address 
        amount
        end_time
        delayed
    """

    type_amino = "cosmos-sdk/MsgCreateVestingAccount"
    type_url = "/cosmos.vesting.v1beta1.MsgCreateVestingAccount"
    prototype = MsgCreateVestingAccount_pb

    from_address: AccAddress = attr.ib()
    to_address: AccAddress = attr.ib()
    amount: Coins = attr.ib(converter=Coins)
    end_time: int = attr.ib()
    delayed: bool = attr.ib()

    def to_amino(self) -> dict :
        return {
            "type": self.type_amino,
            "value": {
                "from_address": self.from_address,
                "to_address": self.to_address,
                "amount": self.amount.to_amino(),
                "end_time" : str(self.end_time),
                "delayed" : self.delayed
            },
        }

    @classmethod
    def from_data(cls, data:dict) -> MsgCreateVestingAccount:
        return cls(
            from_address=data["from_address"],
            to_address=data["to_address"],
            amount=Coins.from_data(data["amount"]),
            end_time=int(data["end_time"]),
            delayed=data["delayed"]
        )
    
    def to_data(self) -> dict :
        return {
            "@type": self.type_url,
            "from_address": self.from_address,
            "to_address": self.to_address,
            "amount": self.amount.to_data(),
            "end_time": str(self.end_time),
            "delayed" : self.delayed
        }

    @classmethod
    def from_proto(cls, proto : MsgCreateVestingAccount_pb) -> MsgCreateVestingAccount:
        return cls(
            from_address = proto.from_address,
            to_address = proto.to_address,
            amount = Coins.from_proto(proto.amount),
            end_time = proto.end_time,
            delayed = proto.delayed
        )
    
    def to_proto(self) -> MsgCreateVestingAccount_pb :
        proto = MsgCreateVestingAccount_pb()
        proto.from_address = self.from_address
        proto.to_address = self.to_address
        proto.amount = [c.to_proto() for c in self.amount]
        proto.end_time = self.end_time
        proto.delayed = self.delayed
        return proto

@attr.s
class MsgCreatePeriodicVestingAccount(Msg):
    """MsgCreatePeriodicVestingAccount defines a message that enables creating a vesting.
    
    Args:
        from_address
        to_address
        start_time
        vesting_periods
    """

    type_amino = "cosmos-sdk/MsgCreatePeriodicVestingAccount"
    type_url = "/cosmos.vesting.v1beta1.MsgCreatePeriodicVestingAccount"
    prototype = MsgCreatePeriodicVestingAccount_pb

    from_address: AccAddress = attr.ib()
    to_address: AccAddress = attr.ib()
    start_time: int = attr.ib()
    vesting_periods: List[Period] = attr.ib()

    def to_amino(self) -> dict :
        return {
            "type": self.type_amino,
            "value": {
                "from_address": self.from_address,
                "to_address": self.to_address,
                "start_time": str(self.start_time),
                "vesting_periods": [vp.to_amino() for vp in self.vesting_periods]
            },
        }

    @classmethod
    def from_data(cls, data:dict) -> MsgCreatePeriodicVestingAccount:
        return cls(
            from_address=data["from_address"],
            to_address=data["to_address"],
            start_time=int(data["start_time"]),
            vesting_periods=[Period.from_data(vp) for vp in data["vesting_periods"]]
        )
    
    def to_data(self) -> dict :
        return {
            "@type": self.type_url,
            "from_address": self.from_address,
            "to_address": self.to_address,
            "start_time" : str(self.start_time),
            "vesting_periods": [vp.to_data() for vp in self.vesting_periods]
        }

    @classmethod
    def from_proto(cls, proto : MsgCreatePeriodicVestingAccount_pb) -> MsgCreatePeriodicVestingAccount:
        return cls(
            from_address = proto.from_address,
            to_address = proto.to_address,
            start_time = proto.start_time,
            vesting_periods = [Period.from_proto(vs) for vs in proto.vesting_periods]
        )
    
    def to_proto(self) -> MsgCreatePeriodicVestingAccount_pb :
        proto = MsgCreatePeriodicVestingAccount_pb()
        proto.from_address = self.from_address
        proto.to_address = self.to_address
        proto.start_time = self.start_time
        proto.vesting_periods = [vp.to_proto for vp in self.vesting_periods]
        return proto

@attr.s
class MsgDonateAllVestingTokens(Msg):
    """MsgDonateAllVestingTokens defines a message that enables donating all vesting.
    
    Args:
        from_address
    """

    type_amino = "cosmos-sdk/MsgDonateAllVestingTokens"
    type_url = "/cosmos.vesting.v1beta1.MsgDonateAllVestingTokens"
    prototype = MsgDonateAllVestingTokens_pb

    from_address: AccAddress = attr.ib()

    def to_amino(self) -> dict :
        return {
            "type": self.type_amino,
            "value": {
                "from_address": self.from_address,
            },
        }

    @classmethod
    def from_data(cls, data:dict) -> MsgDonateAllVestingTokens:
        return cls(
            from_address=data["from_address"],
        )
    
    def to_data(self) -> dict :
        return {
            "@type": self.type_url,
            "from_address": self.from_address,
        }

    @classmethod
    def from_proto(cls, proto : MsgDonateAllVestingTokens_pb) -> MsgDonateAllVestingTokens:
        return cls(
            from_address = proto.from_address,
        )
    
    def to_proto(self) -> MsgDonateAllVestingTokens_pb :
        proto = MsgDonateAllVestingTokens_pb()
        proto.from_address = self.from_address
        return proto
