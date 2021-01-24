from __future__ import annotations

from bech32 import bech32_decode, bech32_encode

__all__ = [
    "AccAddress",
    "ValAddress",
    "ValConsAddress",
    "AccPubKey",
    "ValPubKey",
    "ValConsPubKey",
]


def check_prefix_and_length(prefix: str, data: str, length: int):
    vals = bech32_decode(data)
    return vals[0] == prefix and len(data) == length


def is_val_address(data: str) -> bool:
    return (
        is_bech32(data)
        and data.startswith("terravaloper")
        and not data.startswith("terravaloperpub")
    )


def is_val_consaddress(data: str) -> bool:
    return (
        is_bech32(data)
        and data.startswith("terravalcons")
        and not data.startswith("terravalconspub")
    )


def is_acc_pubkey(data: str) -> bool:
    return is_bech32(data) and data.startswith("terrapub")


def is_val_pubkey(data: str) -> bool:
    return is_bech32(data) and data.startswith("terravalpub")


def is_val_conspubkey(data: str) -> bool:
    return is_bech32(data) and data.startswith("terravalconspub")


class AccAddress(str):
    @staticmethod
    def validate(data: str) -> bool:
        return check_prefix_and_length("terra", data, 44)

    @staticmethod
    def from_val_address(data: str) -> str:
        vals = bech32_decode(data)
        return bech32_encode("terra", vals[1])


class ValAddress(str):
    @staticmethod
    def validate(data: str) -> bool:
        return check_prefix_and_length("terravaloper", data, 51)

    @staticmethod
    def from_val_address(data: str) -> str:
        vals = bech32_decode(data)
        return bech32_encode("terravaloper", vals[1])


class AccPubKey(str):
    @staticmethod
    def validate(data: str) -> bool:
        return check_prefix_and_length("terrapub", 76)

    @staticmethod
    def from_val_pubkey(data: str) -> str:
        vals = bech32_decode(data)
        return bech32_encode("terrapub", vals[1])


class ValPubKey(str):
    @staticmethod
    def validate(data: str) -> bool:
        return check_prefix_and_length("terravaloperpub", data, 83)

    @staticmethod
    def from_val_address(data: str) -> str:
        vals = bech32_decode(data)
        return bech32_encode("terravaloperpub", vals[1])


class ValConsPubKey(str):
    @staticmethod
    def validate(data: str) -> bool:
        return check_prefix_and_length("terravalconspub", data, 83)