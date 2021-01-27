import abc
import json
import copy

from typing import Any


def to_data(x: Any) -> Any:
    if "to_data" in dir(x):
        return x.to_data()
    if isinstance(x, list):
        return [to_data(g) for g in x]
    return x


def dict_to_data(d: dict) -> Any:
    """Recursively calls to_data on dict"""
    return {key: to_data(d[key]) for key in d}


class JSONSerializable:
    @abc.abstractmethod
    def to_data(self) -> dict:
        return dict_to_data(copy.deepcopy(self.__dict__))

    def to_json(self) -> str:
        return json.dumps(self.to_data(), sort_keys=True, separators=(",", ":"))
