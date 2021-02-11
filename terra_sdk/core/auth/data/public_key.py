from __future__ import annotations

from typing import Optional, Union

import attr

from terra_sdk.util.json import JSONSerializable

__all__ = ["PublicKey"]


@attr.s
class PublicKey(JSONSerializable):
    """Data object holding the public key component of an account or signature."""

    SIMPLE: str = "tendermint/PubKeySecp256k1"
    """Normal signature public key type."""

    MULTISIG: str = "tendermint/PubKeyMultisigThreshold"
    """Multisig public key type."""

    type: str = attr.ib()
    """Either :data:`PublicKey.SIMPLE` or :data:`PublicKey.MULTISIG`."""

    value: Optional[Union[str, dict]] = attr.ib()
    """"""

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
        if data is None:
            return None
        return cls(data["type"], data.get("value"))
