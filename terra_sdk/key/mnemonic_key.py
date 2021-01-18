from __future__ import annotations

import hashlib

from ecdsa import SECP256k1, SigningKey
from ecdsa.util import sigencode_string_canonize
from mnemonic import Mnemonic

from terra_sdk.key import Key, derive_child, derive_root, LUNA_COIN_TYPE

__all__ = ["MnemonicKey"]


class MnemonicKey(Key):
    """Implements Key interface with 24-word mnemonic. This implementation exposes the private
    key inside the application, and may not be suited for situations that demand high security."""

    def __init__(
        self,
        mnemonic: str,
        account: int = 0,
        index: int = 0,
        coin_type: int = LUNA_COIN_TYPE,
    ):
        self.mnemonic = mnemonic
        seed = Mnemonic("english").to_seed(self.mnemonic)
        root = derive_root(seed)
        child = derive_child(root, account, index, coin_type)
        self.account = account
        self.index = index
        self._private_key = child.PrivateKey()
        self._public_key = child.PublicKey()

    @property
    def public_key(self) -> bytes:
        return self._public_key

    @classmethod
    def generate(
        cls, account: int = 0, index: int = 0, coin_type: int = LUNA_COIN_TYPE
    ) -> MnemonicKey:
        """Generate a random Mnemonic, with the private / public key pair with the BIP44 HD Path
        located at 44'/330'/<account>'/0/<index> (LUNA)."""
        return cls(
            mnemonic=Mnemonic("english").generate(256),
            account=account,
            index=index,
            coin_type=coin_type,
        )

    def sign(self, payload: bytes) -> bytes:
        """Sign a payload using ECDSA curve SECP256k1."""
        sk = SigningKey.from_string(self._private_key, curve=SECP256k1)
        return sk.sign_deterministic(
            payload, hashfunc=hashlib.sha256, sigencode=sigencode_string_canonize,
        )
