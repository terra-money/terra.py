"""Some useful base classes to inherit from."""

from typing import Any

from .json import dict_to_data


class BaseTerraData(object):

    type: str

    def to_data(self) -> dict:
        if "object_value" in dir(self):
            value = self.object_value()
        else:
            value = dict_to_data(self.__dict__)
        return {"type": self.type, "value": dict_to_data(self.__dict__)}
