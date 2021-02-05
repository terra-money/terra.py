from __future__ import annotations

from bip32utils import BIP32_HARDEN, BIP32Key
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
        mnemonic: str = None,
        account: int = 0,
        index: int = 0,
        coin_type: int = LUNA_COIN_TYPE,
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
