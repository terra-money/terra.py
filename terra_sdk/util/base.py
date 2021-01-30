"""Some useful base classes to inherit from."""

from typing import List, Dict, Any, Callable

from .json import dict_to_data, JSONSerializable


class BaseTerraData(JSONSerializable):

    type: str

    def to_data(self) -> dict:
        if "object_value" in dir(self):
            value = self.object_value()
        else:
            value = dict_to_data(self.__dict__)
        return {"type": self.type, "value": dict_to_data(self.__dict__)}


def create_demux(inputs: List) -> Dict[str, Callable[[dict], Any]]:
    table = {i.type: i.from_data for i in inputs}

    def from_data(data: dict):
        return table[data["type"]](data)

    return from_data
