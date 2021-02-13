import abc
import base64
import hashlib
from typing import Optional

from bech32 import bech32_encode, convertbits

from terra_sdk.core import AccAddress, AccPubKey, ValAddress, ValPubKey
from terra_sdk.core.auth import StdSignature, StdSignMsg, StdTx

BECH32_PUBKEY_DATA_PREFIX = "eb5ae98721"

__all__ = ["Key"]


def get_bech(prefix: str, payload: str) -> str:
    data = convertbits(bytes.fromhex(payload), 8, 5)
    if data is None:
        raise ValueError(f"could not parse data: prefix {prefix}, payload {payload}")
    return bech32_encode(prefix, data)  # base64 -> base32


def address_from_public_key(public_key: bytes) -> bytes:
    sha = hashlib.sha256()
    rip = hashlib.new("ripemd160")
    sha.update(public_key)
    rip.update(sha.digest())
    return rip.digest()


def pubkey_from_public_key(public_key: bytes) -> bytes:
    arr = bytearray.fromhex(BECH32_PUBKEY_DATA_PREFIX)
    arr += bytearray(public_key)
    return bytes(arr)


class Key:
    """Abstract Key interface, representing an agent with transaction-signing capabilities.

    Args:
        public_key (Optional[bytes]): compressed public key bytes,
    """

    public_key: Optional[bytes]
    """Compressed public key bytes, used to derive :data:`raw_address` and :data:`raw_pubkey`."""

    raw_address: Optional[bytes]
    """Raw Bech32 words of address, used to derive associated account and validator
    operator addresses.
    """

    raw_pubkey: Optional[bytes]
    """Raw Bech32 words of pubkey, used to derive associated account and validator
    pubkeys.
    """

    def __init__(self, public_key: Optional[bytes] = None):
        self.public_key = public_key
        if public_key:
            self.raw_address = address_from_public_key(public_key)
            self.raw_pubkey = pubkey_from_public_key(public_key)

    @abc.abstractmethod
    def sign(self, payload: bytes) -> bytes:
        """Signs the data payload. An implementation of Key is expected to override this method.

        Args:
            payload (bytes): arbitrary data payload

        Raises:
            NotImplementedError: if not implemented

        Returns:
            bytes: signed payload
        """
        raise NotImplementedError("an instance of Key must implement Key.sign")

    @property
    def acc_address(self) -> AccAddress:
        """Terra Bech32 account address. Default derivation via :data:`public_key` is provided.

        Raises:
            ValueError: if Key was not initialized with proper public key

        Returns:
            AccAddress: account address
        """
        if not self.raw_address:
            raise ValueError("could not compute acc_address: missing raw_address")
        return AccAddress(get_bech("terra", self.raw_address.hex()))

    @property
    def val_address(self) -> ValAddress:
        """Terra Bech32 validator operator address. Default derivation via :data:`public_key` is provided.

        Raises:
            ValueError: if Key was not initialized with proper public key

        Returns:
            ValAddress: validator operator address
        """
        if not self.raw_address:
            raise ValueError("could not compute val_address: missing raw_address")
        return ValAddress(get_bech("terravaloper", self.raw_address.hex()))

    @property
    def acc_pubkey(self) -> AccPubKey:
        """Terra Bech32 account pubkey. Default derivation via :data:`public_key` is provided.

        Raises:
            ValueError: if Key was not initialized with proper public key

        Returns:
            AccPubKey: account pubkey
        """
        if not self.raw_pubkey:
            raise ValueError("could not compute acc_pubkey: missing raw_pubkey")
        return AccPubKey(get_bech("terrapub", self.raw_pubkey.hex()))

    @property
    def val_pubkey(self) -> ValPubKey:
        """Terra Bech32 validator pubkey. Default derivation via ``public_key`` is provided.

        Raises:
            ValueError: if Key was not initialized with proper public key

        Returns:
            ValPubKey: validator pubkey
        """
        if not self.raw_pubkey:
            raise ValueError("could not compute val_pubkey: missing raw_pubkey")
        return ValPubKey(get_bech("terravaloperpub", self.raw_pubkey.hex()))

    def create_signature(self, tx: StdSignMsg) -> StdSignature:
        """Signs the transaction with the signing algorithm provided by this Key implementation,
        and outputs the signature. The signature is only returned, and must be manually added to
        the ``signatures`` field of an :class:`StdTx`.

        Args:
            tx (StdSignMsg): unsigned transaction

        Raises:
            ValueError: if missing ``public_key``

        Returns:
            StdSignature: signature object
        """
        if self.public_key is None:
            raise ValueError(
                "signature could not be created: Key instance missing public_key"
            )

        sig_buffer = self.sign(tx.to_json().strip().encode())
        return StdSignature.from_data(
            {
                "signature": base64.b64encode(sig_buffer).decode(),
                "pub_key": {
                    "type": "tendermint/PubKeySecp256k1",
                    "value": base64.b64encode(self.public_key).decode(),
                },
            }
        )

    def sign_tx(self, tx: StdSignMsg) -> StdTx:
        """Signs the transaction with the signing algorithm provided by this Key implementation,
        and creates a ready-to-broadcast :class:`StdTx` object with the signature applied.

        Args:
            tx (StdSignMsg): unsigned transaction

        Returns:
            StdTx: ready-to-broadcast transaction object
        """
        sig = self.create_signature(tx)
        return StdTx(tx.msgs, tx.fee, [sig], tx.memo)
