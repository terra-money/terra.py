import os

import bech32

from terra_sdk.error import (
    InvalidAccAddress,
    InvalidAccPubKey,
    InvalidValAddress,
    InvalidValConsAddress,
    InvalidValConsPubKey,
    InvalidValPubKey,
    ValidationError,
)


def is_bech32(data: str) -> bool:
    # ignore if we are testing
    if os.environ.get("terra_sdk_BECH32_VALIDATE", "1") == "0":
        return True
    return bech32.bech32_decode(data) != (None, None,)


def is_acc_address(data: str) -> bool:
    return (
        is_bech32(data)
        and data.startswith("terra")
        and not data.startswith("terravaloper")
        and not data.startswith("terravalcons")
        and not data.startswith("terrapub")
        and not data.startswith("terravalpub")
        and not data.startswith("terravalconspub")
    )


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


def validate_acc_address(data) -> str:
    """Tries to exctract an account address from the object."""
    if hasattr(data, "acc_address"):
        data = data.acc_address
    elif hasattr(data, "address"):
        data = data.address
    if not is_acc_address(data):
        raise InvalidAccAddress(data)
    return data


def validate_val_address(data) -> str:
    """Tries to exctract a validator operator address from the object."""
    if hasattr(data, "val_address"):
        data = data.val_address
    if not is_val_address(data):
        raise InvalidValAddress(data)
    return data


def validate_val_consaddress(data: str) -> str:
    if not is_val_consaddress(data):
        raise InvalidValConsAddress(data)
    return data


def validate_acc_pubkey(data: str) -> str:
    if not is_acc_pubkey(data):
        raise InvalidAccPubKey(data)
    return data


def validate_val_pubkey(data: str) -> str:
    if not is_val_pubkey(data):
        raise InvalidValPubKey(data)
    return data


def validate_val_conspubkey(data: str) -> str:
    if not is_val_conspubkey(data):
        raise InvalidValConsPubKey(data)
    return data


def validate_same_denom(d1: str, d2: str) -> None:
    if not d1 == d2:
        raise ValidationError(f"Denom '{d1}' != '{d2}', aborting.")


class Schemas(object):
    ACC_ADDRESS = {"type": "string", "pattern": r"^terra[a-zA-Z0-9]{39}\Z"}
    VAL_ADDRESS = {"type": "string", "pattern": r"^terravaloper[a-zA-Z0-9]{39}\Z"}
    VAL_CONSADDRESS = {"type": "string", "pattern": r"^terravalcons[a-zA-Z0-9]{39}\Z"}
    ACC_PUBKEY = {"type": "string", "pattern": r"^terrapub[a-zA-Z0-9]{67}\Z"}
    VAL_PUBKEY = {"type": "string", "pattern": r"^terravalpub[a-zA-Z0-9]{67}\Z"}
    VAL_CONSPUBKEY = {"type": "string", "pattern": r"^terravalconspub[a-zA-Z0-9]{67}\Z"}

    STRING = {"type": "string"}
    STRING_INTEGER = {"type": "string", "pattern": r"^[\+\-]?[0-9]+\Z"}
    INTEGER = {"type": "integer"}
    BOOLEAN = {"type": "boolean"}
    OBJ = {"type": "object"}  # generic object

    @staticmethod
    def STRING_WITH_PATTERN(pattern: str):
        return {"type": "string", "pattern": pattern}

    @staticmethod
    def STRING_ENUM(*options):
        return {"type": "string", "enum": options}

    @staticmethod
    def ANY(*schemas):
        return {"anyOf": list(schemas)}

    @staticmethod
    def ONE(*schemas):
        return {"oneOf": list(schemas)}

    @staticmethod
    def ALL(*schemas):
        return {"allOf": list(schemas)}

    @staticmethod
    def OPTIONAL(schema):
        return {"anyOf": [schema, {"type": "null"}]}

    @staticmethod
    def OBJECT(**kwargs) -> object:
        return {
            "type": "object",
            "properties": kwargs,
            "required": list(kwargs.keys()),
        }

    @staticmethod
    def ARRAY(schema, **kwargs):
        return {"type": "array", "items": schema, **kwargs}
