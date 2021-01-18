"""Some useful base classes to inherit from."""

from typing import Any


def to_data(x: Any) -> Any:
    if "to_data" in dir(x):
        return x.to_data()
    else:
        x


class BaseTerraData(object):

    type: str

    def to_data(self) -> dict:
        if "object_value" in dir(self):
            value = self.object_value()
        else:
            value = to_data(self.__dict__)
        return {
            "type": self.type,
            "value": to_data(self.__dict__)
        }
