from __future__ import annotations

from typing import NewType

from bech32 import bech32_decode, bech32_encode

__all__ = [
    "AccAddress",
    "ValAddress",
    "AccPubKey",
    "ValPubKey",
    "ValConsPubKey",
    "is_acc_address",
    "is_acc_pubkey",
    "is_val_address",
    "is_val_pubkey",
    "is_valcons_pubkey",
    "to_acc_address",
    "to_acc_pubkey",
    "to_val_address",
    "to_val_pubkey",
]


def check_prefix_and_length(prefix: str, data: str, length: int):
    vals = bech32_decode(data)
    return vals[0] == prefix and len(data) == length


AccAddress = NewType("AccAddress", str)
ValAddress = NewType("ValAddress", str)
AccPubKey = NewType("AccPubKey", str)
ValPubKey = NewType("ValPubKey", str)
ValConsPubKey = NewType("ValConsPubKey", str)


def is_acc_address(data: str) -> bool:
    return check_prefix_and_length("terra", data, 44)


def to_acc_address(data: ValAddress) -> AccAddress:
    vals = bech32_decode(data)
    if vals[1] is None:
        raise ValueError(f"invalid bech32: {data}")
    return AccAddress(bech32_encode("terra", vals[1]))


def is_val_address(data: str) -> bool:
    return check_prefix_and_length("terravaloper", data, 51)


def to_val_address(data: AccAddress) -> ValAddress:
    vals = bech32_decode(data)
    if vals[1] is None:
        raise ValueError(f"invalid bech32: {data}")
    return ValAddress(bech32_encode("terravaloper", vals[1]))


def is_acc_pubkey(data: str) -> bool:
    return check_prefix_and_length("terrapub", data, 76)


def to_acc_pubkey(data: ValPubKey) -> AccPubKey:
    vals = bech32_decode(data)
    if vals[1] is None:
        raise ValueError(f"invalid bech32: {data}")
    return AccPubKey(bech32_encode("terrapub", vals[1]))


def is_val_pubkey(data: str) -> bool:
    return check_prefix_and_length("terravaloperpub", data, 83)


def to_val_pubkey(data: AccPubKey) -> ValPubKey:
    vals = bech32_decode(data)
    if vals[1] is None:
        raise ValueError(f"invalid bech32: {data}")
    return ValPubKey(bech32_encode("terravaloperpub", vals[1]))


def is_valcons_pubkey(data: str) -> ValConsPubKey:
    return check_prefix_and_length("terravalconspub", data, 83)
