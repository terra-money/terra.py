import copy
import json
from abc import ABC
from datetime import datetime
from typing import Any

from terra_sdk.util.converter import to_isoformat


def to_data(x: Any) -> Any:
    if hasattr(x, "to_data"):
        return x.to_data()
    if isinstance(x, int):
        return str(x)
    if isinstance(x, datetime):
        return to_isoformat(x)
    if isinstance(x, list):
        return [to_data(g) for g in x]
    if isinstance(x, dict):
        return dict_to_data(x)
    if isinstance(x, datetime):
        return to_isoformat(x)
    return x


def to_amino(x: Any) -> Any:
    if "to_amino" in dir(x):
        return x.to_amino()
    if isinstance(x, list):
        return [to_data(g) for g in x]
    if isinstance(x, datetime):
        return to_isoformat(x)
    if isinstance(x, dict):
        return dict_to_amino(x)
    if isinstance(x, int):
        return str(x)
    if isinstance(x, datetime):
        return to_isoformat(x)


def dict_to_amino(d: dict):
    return {key: to_amino(d[key]) for key in d}


def dict_to_data(d: dict) -> dict:
    """Recursively calls to_data on dict"""
    return {key: to_data(d[key]) for key in d}


class JSONSerializable(ABC):
    def to_data(self) -> Any:
        """Converts the object to its JSON-serializable Python data representation."""
        return dict_to_data(copy.deepcopy(self.__dict__))

    def to_json(self) -> str:
        """Marshals the object into a stringified JSON serialization. Keys are first sorted
        and the JSON rendered removes all unnecessary whitespace.

        Returns:
           str: JSON string representation
        """
        return json.dumps(self.to_data(), sort_keys=True, separators=(",", ":"))
