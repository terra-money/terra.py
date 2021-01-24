from __future__ import annotations

import hashlib
from bip32utils import BIP32Key, BIP32_HARDEN
from mnemonic import Mnemonic

from .raw import RawKey

__all__ = ["MnemonicKey", "LUNA_COIN_TYPE"]

LUNA_COIN_TYPE = 330


class MnemonicKey(RawKey):

    mnemonic: str
    account: int
    index: int
    coin_type = int

    def __init__(
        self,
        mnemonic: Optional[str] = None,
        account: Optional[int] = 0,
        index: Optional[int] = 0,
        coin_type: Optional[int] = LUNA_COIN_TYPE,
    ):
        if mnemonic is None:
            mnemonic = Mnemonic("english").generate(256)
        seed = Mnemonic("english").to_seed(mnemonic)
        root = BIP32Key.fromEntropy(seed)
        # derive from hdpath
        child = (
            root.ChildKey(44 + BIP32_HARDEN)
            .ChildKey(coin_type + BIP32_HARDEN)
            .ChildKey(account + BIP32_HARDEN)
            .ChildKey(0)
            .ChildKey(index)
        )

        super().__init__(child.PrivateKey())
        self.mnemonic = mnemonic
        self.account = account
        self.index = index
