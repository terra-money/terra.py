import hashlib

from ecdsa import SECP256k1, SigningKey
from ecdsa.util import sigencode_string_canonize

from .key import Key

__all__ = ["RawKey"]


def compute_public_key(private_key: bytes) -> bytes:
    return (
        SigningKey.from_string(private_key, curve=SECP256k1)
        .get_verifying_key()
        .to_string("compressed")
    )


class RawKey(Key):

    private_key: bytes

    def __init__(self, private_key: bytes):
        public_key = compute_public_key(private_key)
        super().__init__(public_key)
        self.private_key = private_key

    def sign(self, payload: bytes) -> bytes:
        sk = SigningKey.from_string(self.private_key, curve=SECP256k1)
        return sk.sign_deterministic(
            payload,
            hashfunc=hashlib.sha256,
            sigencode=sigencode_string_canonize,
        )
