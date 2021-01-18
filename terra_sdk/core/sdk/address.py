from __future__ import annotations

from bech32 import bech32_decode, bech32_encode

from terra_sdk.util.validation import (
    validate_acc_address,
    validate_val_address,
    validate_val_consaddress
)

__all__ = ["AccAddress", "ValAddress", "ValConsAddress"]


class AccAddress(str):
    """`terra-` prefixed Bech32-enconded account address, works anywhere a `str` is
    accepted but will perform verification on the checksum.

    :param arg: string-convertable object to convert.
    """

    def __new__(cls, arg):
        arg = validate_acc_address(arg)
        return str.__new__(cls, arg)

    @property
    def val_address(self) -> ValAddress:
        """The associated validator operator address."""
        decoded = bech32_decode(self)
        return ValAddress(bech32_encode("terravaloper", decoded[1]))


class ValAddress(str):
    """`terravaloper-` prefixed Bech32-enconded account address, works anywhere a `str`
    is accepted but will perform verification on the checksum.

    :param arg: string-convertable object to convert.
    """

    def __new__(cls, arg):
        arg = validate_val_address(arg)
        return str.__new__(cls, arg)

    @property
    def acc_address(self) -> AccAddress:
        """The associated account address."""
        decoded = bech32_decode(self)
        return AccAddress(bech32_encode("terra", decoded[1]))


class ValConsAddress(str):
    """`terravalcons-` prefixed Bech32-enconded consensus address, works anywhere a `str`
    is accepted but will perform verification on the checksum.

    :param arg: string-convertable object to convert.
    """

    def __new__(cls, arg):
        validate_val_consaddress(arg)
        return str.__new__(cls, arg)
