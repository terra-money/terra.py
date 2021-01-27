from __future__ import annotations

import attr

__all__ = ["PublicKey"]


@attr.s
class PublicKey:

    SIMPLE = "tendermint/PubKeySecp256k1"
    MULTISIG = "tendermint/PubKeyMultisigThreshold"

    type: str = attr.ib()
    value: Union[str, dict] = attr.ib()

    def to_data(self) -> dict:
        if self.type == self.SIMPLE and isinstance(self.value, str):
            return {"type": self.type, "value": self.value}
        elif self.type == self.MULTISIG and not isinstance(self.value, str):
            return {"type": self.type, "value": self.value}
        else:
            raise TypeError(
                f"could not marshal PublicKey: type and value are incorrect {self.type} {self.value}"
            )

    @classmethod
    def from_data(cls, data: dict) -> PublicKey:
        return cls(data.get("type"), data.get("value"))