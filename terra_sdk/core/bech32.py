"""Special Bech32 String Types"""

from __future__ import annotations

from typing import NewType

from bech32 import bech32_decode, bech32_encode, convertbits

__all__ = [
    "AccAddress",
    "ValAddress",
    "AccPubKey",
    "ValPubKey",
    "is_acc_address",
    "is_acc_pubkey",
    "is_val_address",
    "is_val_pubkey",
    "is_valcons_pubkey",
    "to_acc_address",
    "to_acc_pubkey",
    "to_val_address",
    "to_val_pubkey",
    "get_bech",
]


def get_bech(prefix: str, payload: str) -> str:
    data = convertbits(bytes.fromhex(payload), 8, 5)
    if data is None:
        raise ValueError(f"could not parse data: prefix {prefix}, payload {payload}")
    return bech32_encode(prefix, data)  # base64 -> base32


def check_prefix_and_length(prefix: str, data: str, length: int):
    vals = bech32_decode(data)
    return vals[0] == prefix and len(data) == length


AccAddress = NewType("AccAddress", str)
AccAddress.__doc__ = """Terra Bech32 Account Address -- type alias of str."""

ValAddress = NewType("ValAddress", str)
ValAddress.__doc__ = """Terra Bech32 Validator Operator Address -- type alias of str."""

AccPubKey = NewType("AccPubKey", str)
AccPubKey.__doc__ = """Terra Bech32 Account Address -- type alias of str."""

ValPubKey = NewType("ValPubKey", str)
ValPubKey.__doc__ = """Terra Bech32 Validator PubKey -- type alias of str."""

# ValConsPubKey = NewType("ValConsPubKey", str)
# ValConsPubKey.__doc__ = (
#  """Terra Bech32 Validator Conensus PubKey -- type alias of str."""
# )


def is_acc_address(data: str) -> bool:
    """Checks whether the given string is a properly formatted Terra account address.

    Args:
        data (str): string to check

    Returns:
        bool: whether the string is a proper account address
    """
    return check_prefix_and_length("terra", data, 44)


def to_acc_address(data: ValAddress) -> AccAddress:
    """Converts a validator operator address into an account address.

    Args:
        data (ValAddress): validator operator address

    Raises:
        ValueError: if provided string is not Bech32

    Returns:
        AccAddress: account address
    """
    vals = bech32_decode(data)
    if vals[1] is None:
        raise ValueError(f"invalid bech32: {data}")
    return AccAddress(bech32_encode("terra", vals[1]))


def is_val_address(data: str) -> bool:
    """Checks whether the given string is a properly formatted Terra validator operator
    address.

    Args:
        data (str): string to check

    Returns:
        bool: whether the string is a proper validator address
    """
    return check_prefix_and_length("terravaloper", data, 51)


def to_val_address(data: AccAddress) -> ValAddress:
    """Converts an account address into a validator operator address.

    Args:
        data (AccAddress): account address

    Raises:
        ValueError: if provided string is not Bech32

    Returns:
        ValAddress: validator operator address
    """
    vals = bech32_decode(data)
    if vals[1] is None:
        raise ValueError(f"invalid bech32: {data}")
    return ValAddress(bech32_encode("terravaloper", vals[1]))


def is_acc_pubkey(data: str) -> bool:
    """Checks whether the provided string is a properly formatted Terra account pubkey.

    Args:
        data (str): string to check

    Returns:
        bool: whether string is account pubkey
    """
    return check_prefix_and_length("terrapub", data, 76)


def to_acc_pubkey(data: ValPubKey) -> AccPubKey:
    """Converts a validator pubkey into an account pubkey.

    Args:
        data (ValPubKey): validator pubkey

    Raises:
        ValueError: if provided string is not Bech32

    Returns:
        AccPubKey: account pubkey
    """
    vals = bech32_decode(data)
    if vals[1] is None:
        raise ValueError(f"invalid bech32: {data}")
    return AccPubKey(bech32_encode("terrapub", vals[1]))


def is_val_pubkey(data: str) -> bool:
    """Checks whether provided string is a properly formatted Terra validator pubkey.

    Args:
        data (str): string to check

    Returns:
        bool: whether string is validator pubkey
    """
    return check_prefix_and_length("terravaloperpub", data, 83)


def to_val_pubkey(data: AccPubKey) -> ValPubKey:
    """Converts an account pubkey into a validator pubkey.

    Args:
        data (AccPubKey): account pubkey

    Raises:
        ValueError: if provided string is not Bech32

    Returns:
        ValPubKey: validator pubkey
    """
    vals = bech32_decode(data)
    if vals[1] is None:
        raise ValueError(f"invalid bech32: {data}")
    return ValPubKey(bech32_encode("terravaloperpub", vals[1]))


def is_valcons_pubkey(data: str) -> bool:  # -> ValConsPubKey:
    """Checks whether provided string is a properly formatted Terra validator consensus
    pubkey.

    Args:
        data (str): string to check

    Returns:
        bool: whether string is validator consensus pubkey
    """
    return check_prefix_and_length("terravalconspub", data, 83)
