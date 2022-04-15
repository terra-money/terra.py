"""Some useful base classes to inherit from."""
from abc import abstractmethod
from typing import Any, Callable, Dict, List
from betterproto.lib.google.protobuf import Any as Any_pb
from betterproto import Message

from .json import JSONSerializable, dict_to_data


class BaseTerraData(JSONSerializable, Message):

    type: str
    type_url: str

    def to_data(self) -> dict:
        return {"type": self.type_url, "value": dict_to_data(self.__dict__)}

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
