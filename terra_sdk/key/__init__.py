import abc
import base64
import hashlib
from typing import Union

from bip32utils import BIP32_HARDEN, BIP32Key
from cached_property import cached_property

from terra_sdk.core.auth.transaction import StdSignature, StdSignMsg, StdTx
from terra_sdk.core.sdk.pubkey import PublicKey
from terra_sdk.util import get_bech

BECH32_PUBKEY_DATA_PREFIX = "eb5ae98721"

__all__ = ["derive_child", "derive_root", "LUNA_COIN_TYPE", "Key"]

LUNA_COIN_TYPE = 330


def derive_root(seed: bytes) -> BIP32Key:
    return BIP32Key.fromEntropy(seed)


def derive_child(
    root: BIP32Key, account: int = 0, index: int = 0, coin_type: int = LUNA_COIN_TYPE
):
    # HD Path: 44'/330'/<acc>'/0/<idx>
    return (
        root.ChildKey(44 + BIP32_HARDEN)
        .ChildKey(coin_type + BIP32_HARDEN)
        .ChildKey(account + BIP32_HARDEN)
        .ChildKey(0)
        .ChildKey(index)
    )


class Key(object, metaclass=abc.ABCMeta):
    """Abstract interface for managing a Terra private key / public key pair."""

    @property
    @abc.abstractmethod
    def public_key(self) -> bytes:
        """Get the Key's associated public key."""
        raise NotImplementedError("Keys must implement public_key property")

    @abc.abstractmethod
    def sign(self, payload: bytes) -> bytes:
        """Signs a string payload with the private key."""
        raise NotImplementedError("Keys must implement sign()")

    @cached_property
    def base_address(self) -> bytes:
        """Get's the Key's base address for determining Bech32 acc, val addresses."""
        sha = hashlib.sha256()
        rip = hashlib.new("ripemd160")
        sha.update(self.public_key)
        rip.update(sha.digest())
        return rip.digest()

    def create_signature(self, tx: StdSignMsg) -> StdSignature:
        """Signs a transaction (`StdSignMsg` or `StdTx`), returns a signature."""
        sig_data = self.sign(tx.to_json(sort=True).strip().encode())
        pub_key = PublicKey(value=base64.b64encode(self.public_key).decode())
        return StdSignature(
            signature=base64.b64encode(sig_data).decode(), pub_key=pub_key,
        )

    def sign_tx(self, tx: Union[StdSignMsg, StdTx]) -> StdTx:
        """Creates a signature for the transaction and returns a signed transaction."""
        signature = self.create_signature(tx)
        if isinstance(tx, StdTx):  # if already signed
            tx.signatures.append(signature)
            return tx
        else:
            return StdTx(fee=tx.fee, msg=tx.msgs, signatures=[signature], memo=tx.memo)

    @cached_property
    def acc_address(self) -> str:
        """Get's the key's associated account (terra- prefixed) address."""
        return get_bech("terra", self.base_address.hex())

    @cached_property
    def acc_pubkey(self) -> str:
        """Get's the key's associated Terra public key (terrapub- prefixed)"""
        return get_bech("terrapub", BECH32_PUBKEY_DATA_PREFIX + self.public_key.hex())

    @cached_property
    def val_address(self) -> str:
        """Get's the key's associated validator operator (terravaloper- prefixed) address."""
        return get_bech("terravaloper", self.base_address.hex())

    @cached_property
    def val_pubkey(self) -> str:
        """Get's the key's associated Terra validator public key (terravaloperpub- prefixed)"""
        return get_bech(
            "terravaloperpub", BECH32_PUBKEY_DATA_PREFIX + self.public_key.hex()
        )
