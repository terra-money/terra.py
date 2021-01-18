"""terra_sdk internal utilities for serialization to / deserialization from JSON."""

from __future__ import annotations

import abc
import json
from typing import Any, Generic, TypeVar

import fastjsonschema
from box import Box

from terra_sdk.client.lcd.api import ApiResponse
from terra_sdk.error import JsonSchemaValidationError
from terra_sdk.util.pretty import PrettyPrintable

_cached_schemas = dict()

T = TypeVar("T")


class JsonDeserializable(Generic[T], metaclass=abc.ABCMeta):
    """Abstract base class for objects which define a unmarshalling strategy after being
    deserialized into a Python data type (dict, list, str, etc.) from a JSON string. Can
    be used as a generic type like `JsonDeserializable[dict]` to define the Python data
    type from which the object is reconstructed."""

    __schema__ = {}

    @property
    @abc.abstractmethod
    def __schema__(self) -> dict:
        """Draft-7 compliant JSONSchema for validating inputs expressed as a Python `dict`."""
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def from_data(cls, data: T, *args, **kwargs) -> JsonDeserializable[T]:
        """Deserialize the object from a native Python format

        :param data: Python data object (dict, int, list, etc.)
        :return: unmarshalled object
        """
        raise NotImplementedError

    @classmethod
    def deserialize(cls, data: T, *args, **kwargs) -> JsonDeserializable[T]:
        """Applies JSON Schema-validation checks before attempting to recreate a
        Python object. Calls `from_data()` internally.

        :param data: Python data to construct object from
        :return: unmarshalled object
        :raises: JsonSchemaValidationError: did not pass the schema-validation check
        """
        if cls not in _cached_schemas:
            _cached_schemas[cls] = fastjsonschema.compile(cls.__schema__)
        try:
            if isinstance(data, ApiResponse):
                data = data.__result__
            _cached_schemas[cls](data)  # validate
        except fastjsonschema.JsonSchemaException as e:
            raise JsonSchemaValidationError(
                cls, data, e.message, e.value, e.name, e.definition, e.rule
            )
        return cls.from_data(data, *args, **kwargs)


def serialize_to_json(item: Any, sort: bool = False, debug: bool = False) -> str:
    """Serializes an object using the serialization strategy for `JsonSerializable`.

    :param item: object to serialize
    :type item: Any
    :param sort: sort keys alphabetically
    :type sort: bool
    :param debug: pretty-print indentation
    :type debug: bool
    """
    return json.dumps(
        item,
        indent=2 if debug else None,
        sort_keys=sort,
        separators=(",", ":") if not debug else None,
        cls=terra_sdkJsonEncoder,
    )


class JsonSerializable(PrettyPrintable, Generic[T]):
    """Abstract base class for an object that can be serialized to a JSON string. It should
    define in `.to_data()` how to marshal its contents into a native Python data type whose]
    contents are also normally JSON-serializable, or other instances of `JsonSerializable`.
    Can be used as a type like `JsonSerializable[dict]` or `JsonSerializable[int]` to indicate
    its marshalled data value type immediately prior to conversion to a string.
    """

    def to_data(self) -> T:
        """Override this to define a marshalling strategy. By default, uses a copy of
        the object's `__dict__` property.

        :return: marshalled contents of object
        """
        return dict(self.__dict__)  # copy instead of changing object

    def to_json(self, sort: bool = False, debug: bool = False) -> str:
        """Applies the JSON-serialization strategy to the marshalled contents of the object.

        :param sort: sort by key
        :type sort: bool

        :param debug: pretty-print with indentation
        :type debug: bool

        :return: serialized object as a JSON string
        :rtype: str
        """
        return serialize_to_json(self.to_data(), sort=sort, debug=debug)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, JsonSerializable):
            return self.to_data() == other.to_data()
        else:
            return self.to_data() == other


class terra_sdkJsonEncoder(json.JSONEncoder):
    """Encoder class for `JsonSerializable`"""

    def default(self, o) -> Any:
        if hasattr(o, "to_data"):
            return o.to_data()
        else:
            return json.JSONEncoder.default(self, o)


K = TypeVar("K")  # key
V = TypeVar("V")  # value


class terra_sdkBox(JsonSerializable[dict], Box, Generic[K, V]):
    """JSON-Serializable version of `Box`."""

    def __init__(self, *args, **kwargs):
        Box.__init__(self, *args, **kwargs)

    def __getitem__(self, item: K, _ignore_default: bool = False) -> V:
        return Box.__getitem__(self, item, _ignore_default)

    def __repr__(self) -> str:
        return f"terra_sdkBox{self.to_dict()!r}"

    def to_data(self):
        return self.to_dict()

    @property
    def pretty_header(self):
        return None

    @property
    def pretty_data(self):
        d = self.to_data()
        return list(d.items())
