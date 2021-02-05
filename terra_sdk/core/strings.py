from __future__ import annotations

from bech32 import bech32_decode, bech32_encode

__all__ = [
    "AccAddress",
    "ValAddress",
    "AccPubKey",
    "ValPubKey",
    "ValConsPubKey",
]


def check_prefix_and_length(prefix: str, data: str, length: int):
    vals = bech32_decode(data)
    return vals[0] == prefix and len(data) == length


class AccAddress(str):
    @staticmethod
    def validate(data: str) -> bool:
        return check_prefix_and_length("terra", data, 44)

    @staticmethod
    def from_val_address(data: str) -> str:
        vals = bech32_decode(data)
        if vals[1] is None:
            raise ValueError(f"invalid bech32: {data}")
        return bech32_encode("terra", vals[1])


class ValAddress(str):
    @staticmethod
    def validate(data: str) -> bool:
        return check_prefix_and_length("terravaloper", data, 51)

    @staticmethod
    def from_acc_address(data: str) -> str:
        vals = bech32_decode(data)
        if vals[1] is None:
            raise ValueError(f"invalid bech32: {data}")
        return bech32_encode("terravaloper", vals[1])


class AccPubKey(str):
    @staticmethod
    def validate(data: str) -> bool:
        return check_prefix_and_length("terrapub", data, 76)

    @staticmethod
    def from_val_pubkey(data: str) -> str:
        vals = bech32_decode(data)
        if vals[1] is None:
            raise ValueError(f"invalid bech32: {data}")
        return bech32_encode("terrapub", vals[1])


class ValPubKey(str):
    @staticmethod
    def validate(data: str) -> bool:
        return check_prefix_and_length("terravaloperpub", data, 83)

    @staticmethod
    def from_acc_pubkey(data: str) -> str:
        vals = bech32_decode(data)
        if vals[1] is None:
            raise ValueError(f"invalid bech32: {data}")
        return bech32_encode("terravaloperpub", vals[1])


class ValConsPubKey(str):
    @staticmethod
    def validate(data: str) -> bool:
        return check_prefix_and_length("terravalconspub", data, 83)
