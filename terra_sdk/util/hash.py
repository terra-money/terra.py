import base64
import hashlib

from terra_sdk.core import Tx


def hash_amino(txdata: str) -> str:
    """Get the transaction hash from Amino-encoded Transaction in base64."""
    return hashlib.sha256(base64.b64decode(txdata)).digest().hex()
