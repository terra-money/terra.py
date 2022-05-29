"""Some useful base classes to inherit from."""
from abc import abstractmethod
from typing import Any, Callable, Dict, List

import attr
from betterproto import Message
from betterproto.lib.google.protobuf import Any as Any_pb

from .json import JSONSerializable, dict_to_data


class BaseTerraData(JSONSerializable, Message):

    type: str
    type_url: str

    def to_data(self) -> dict:
        data = dict_to_data(attr.asdict(self))
        data.update({"@type": self.type_url})
        return data

    @abstractmethod
    def to_proto(self):
        pass


# data demux
def create_demux(inputs: List) -> Callable[[Dict[str, Any]], Any]:
    table = {i.type_url: i.from_data for i in inputs}

    def from_data(data: dict):
        return table[data["@type"]](data)

    return from_data


# for other protos inside of msgs
def create_demux_proto(inputs: List) -> Callable[[Dict[str, Any]], Any]:
    table = {i.type_url: i.from_proto for i in inputs}

    def from_proto(proto: Any_pb):
        return table[proto.type_url](proto)

    return from_proto


# Any_pb to Proto for msgs
def create_demux_unpack_any(inputs: List) -> Callable[[Dict[str, Any]], Any]:
    table = {i.type_url: i.from_proto for i in inputs}
    prototypes = {i.type_url: i.prototype for i in inputs}

    def unpack_any(proto: Any_pb):
        return table[proto.type_url](prototypes[proto.type_url]().parse(proto.value))

    return unpack_any


# legacy amino demux
def create_demux_amino(inputs: List) -> Callable[[Dict[str, Any]], Any]:
    table = {i.type_amino: i.from_amino for i in inputs}

    def from_amino(data: dict):
        return table[data["type"]](data)

    return from_amino
