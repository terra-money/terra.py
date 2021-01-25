import abc
import json


class JSONSerializable:
    @abc.abstractmethod
    def to_data(self) -> dict:
        raise NotImplementedError(
            f"to_data() implemented for JSONSerializable instance {self.__name__}"
        )

    def to_json(self) -> str:
        return json.dumps(self.to_data(), sort_keys=True, separators=(",", ":"))
