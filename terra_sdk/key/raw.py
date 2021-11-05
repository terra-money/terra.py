from __future__ import annotations

import hashlib

from ecdsa import SECP256k1, SigningKey
from ecdsa.util import sigencode_string_canonize

from .key import Key

__all__ = ["RawKey"]

from ..core import PublicKey, SimplePublicKey


def compute_public_key(private_key: bytes) -> PublicKey:
    return SimplePublicKey(
        key=SigningKey.from_string(private_key, curve=SECP256k1)
        .get_verifying_key()
        .to_string("compressed")
    )


class RawKey(Key):
    """RawKey directly uses a raw (plaintext) private key in memory, and provides
    the implementation for signing with ECDSA on curve Secp256k1.

    Args:
        private_key (bytes): private key in bytes
    """

    private_key: bytes
    """Private key, in bytes."""

    @classmethod
    def from_hex(cls, private_key_hex: str) -> RawKey:
        """Create a new RawKey from a hex-encoded private key string.

        Args:
            private_key_hex (str): hex-encoded private key
        """
        return cls(bytes.fromhex(private_key_hex))

    def __init__(self, private_key: bytes):
        public_key = compute_public_key(private_key)
        super().__init__(public_key)
        self.private_key = private_key

    def sign(self, payload: bytes) -> bytes:
        """Signs the data payload using ECDSA and curve Secp256k1 with the private key as
        the signing key.

        Args:
            payload (bytes): data to sign
        """
        sk = SigningKey.from_string(self.private_key, curve=SECP256k1)
        return sk.sign_deterministic(
            payload,
            hashfunc=hashlib.sha256,
            sigencode=sigencode_string_canonize,
        )
