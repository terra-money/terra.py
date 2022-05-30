"""feegrant module message types."""

from __future__ import annotations

import attr
from betterproto.lib.google.protobuf import Any as Any_pb
from terra_proto.cosmos.feegrant.v1beta1 import (
    MsgGrantAllowance as MsgGrantAllowance_pb,
)
from terra_proto.cosmos.feegrant.v1beta1 import (
    MsgRevokeAllowance as MsgRevokeAllowance_pb,
)

from terra_sdk.core import AccAddress
from terra_sdk.core.msg import Msg

from .data import Allowance

__all__ = ["MsgGrantAllowance", "MsgRevokeAllowance"]


@attr.s
class MsgGrantAllowance(Msg):
    """
    MsgGrantAllowance adds permission for Grantee to spend up to Allowance
    of fees from the account of Granter.
    """

    granter: AccAddress = attr.ib()
    grantee: AccAddress = attr.ib()
    allowance: Allowance = attr.ib()

    type_amino = "cosmos-sdk/MsgGrantAllowance"
    """"""
    type_url = "/cosmos.feegrant.v1beta1.MsgGrantAllowance"
    """"""
    prototype = MsgGrantAllowance_pb
    """"""

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "granter": self.granter,
                "grantee": self.grantee,
                "allowance": self.allowance.to_amino(),
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "granter": self.granter,
            "grantee": self.grantee,
            "allowance": self.allowance.to_data(),
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgGrantAllowance:
        return cls(
            granter=data["granter"],
            grantee=data["grantee"],
            allowance=Allowance.from_data(data["allowance"]),
        )

    def to_proto(self) -> MsgGrantAllowance_pb:
        return MsgGrantAllowance_pb(
            granter=self.granter,
            grantee=self.grantee,
            allowance=Allowance.pack_any(self.allowance),
        )

    @classmethod
    def from_proto(cls, proto: MsgGrantAllowance_pb) -> MsgGrantAllowance:
        return cls(
            granter=proto.granter,
            grantee=proto.grantee,
            allowance=Allowance.unpack_any(proto.allowance),
        )


@attr.s
class MsgRevokeAllowance(Msg):
    """MsgRevokeAllowance remove permission any existing Allowance from Granter to Grantee."""

    granter: AccAddress = attr.ib()
    grantee: AccAddress = attr.ib()

    type_amino = "cosmos-sdk/MsgRevokeAllowance"
    """"""
    type_url = "/cosmos.feegrant.v1beta1.MsgRevokeAllowance"
    """"""
    prototype = MsgRevokeAllowance_pb
    """"""

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {"granter": self.granter, "grantee": self.grantee},
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgRevokeAllowance:
        return cls(granter=data["granter"], grantee=data["grantee"])

    def to_proto(self) -> MsgRevokeAllowance_pb:
        return MsgRevokeAllowance_pb(granter=self.granter, grantee=self.grantee)

    @classmethod
    def from_proto(cls, proto: MsgRevokeAllowance_pb) -> MsgRevokeAllowance:
        return cls(granter=proto.granter, grantee=proto.grantee)
