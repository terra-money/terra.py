from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from bech32 import bech32_decode, bech32_encode

from terra_sdk.util.serdes import JsonDeserializable, JsonSerializable
from terra_sdk.util.validation import Schemas as S
from terra_sdk.util.validation import (
    validate_acc_pubkey,
    validate_val_conspubkey,
    validate_val_pubkey
)

__all__ = ["PublicKey", "AccPubKey", "ValPubKey", "ValConsPubKey"]


@dataclass
class PublicKey(JsonSerializable, JsonDeserializable):

    type: str = "tendermint/PubKeySecp256k1"
    value: Any = None

    @classmethod
    def from_data(cls, data: dict) -> PublicKey:
        # TODO: apply None-coalescing feature to root JsonDeserializable
        # viz: JsonDeserializable
        if data is None:
            return None
        return cls(type=data["type"], value=data["value"])


class AccPubKey(str):
    """`terrapub-` prefixed Bech32-enconded account public eky, works anywhere a `str` is
    accepted but will perform verification on the checksum.

    :param arg: string-convertable object to convert.
    """

    def __new__(cls, arg):
        validate_acc_pubkey(arg)
        return str.__new__(cls, arg)

    @property
    def val_pubkey(self) -> ValPubKey:
        """The associated validator public key."""
        decoded = bech32_decode(self)
        return ValPubKey(bech32_encode("terravalpub", decoded[1]))


class ValPubKey(str):
    """`terravalpub-` prefixed Bech32-enconded validator public key, works anywhere a `str`
    is accepted but will perform verification on the checksum.

    :param arg: string-convertable object to convert.
    """

    def __new__(cls, arg):
        validate_val_pubkey(arg)
        return str.__new__(cls, arg)

    @property
    def acc_pubkey(self) -> AccPubKey:
        """The associated account public key."""
        decoded = bech32_decode(self)
        return AccPubKey(bech32_encode("terrapub", decoded[1]))


class ValConsPubKey(str):
    """`terravalpub-` prefixed Bech32-enconded validator consensus public key, works \
    anywhere a `str` is accepted but will perform verification on the checksum.

    :param arg: string-convertable object to convert.
    """

    def __new__(cls, arg):
        validate_val_conspubkey(arg)
        return str.__new__(cls, arg)
