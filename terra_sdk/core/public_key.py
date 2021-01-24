from __future__ import annotations

import attr

__all__ = ["PublicKey"]


@attr.s
class PublicKey:

    type: str = attr.ib()
    value: Union[str, dict] = attr.ib()

    def to_data(self) -> dict:
        if self.type == "tendermint/PubKeySecp256k1" and isinstance(self.value, str):
            return {"type": self.type, "value": self.value}
        elif self.type == "tendermint/PubKeyMultisigThreshold" and not isinstance(
            self.value, str
        ):
            return {"type": self.type, "value": self.value}
        else:
            raise TypeError("invalid public key: type and value are incorrect")

    @classmethod
    def from_data(cls, data: dict) -> PublicKey:
        return cls(data.get("type"), data.get("value"))