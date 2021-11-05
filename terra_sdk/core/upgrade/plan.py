"""Upgrade module data objects."""

from __future__ import annotations

__all__ = ["Plan"]

from typing import Optional, Any

import attr
from terra_sdk.util.json import JSONSerializable

from terra_proto.cosmos.upgrade.v1beta1 import Plan as Plan_pb
from betterproto.lib.google.protobuf import Any as Any_pb

from betterproto import datetime

@attr.s
class Plan(JSONSerializable):
    name: str = attr.ib()
    height: str = attr.ib()
    info: str = attr.ib()
    time: Optional[datetime] = attr.ib(default=None, converter=datetime.fromisoformat)
    upgrade_client_state: Optional[Any] = attr.ib(default=None)

    @classmethod
    def from_data(cls, data: dict) -> Plan:
        return cls(
            name=data["name"],
            time=data["time"] if data.get("time") else None,
            height=data["height"],
            info=data["info"],
            upgrade_client_state=data["upgrade_client_state"] if data.get("upgrade_client_state") else None
        )

    def to_proto(self) -> Plan_pb:
        ucs = self.get("upgrade_client_state")
        if ucs is not None:
            ucs = Any_pb(type_url=ucs["type_url"], value=bytes(ucs.to_proto()))
        return Plan_pb(
            name=self.name,
            time=self.time,
            height=self.height,
            info=self.info,
            upgraded_client_state=ucs if ucs else None
        )
