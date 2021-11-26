Keys & Wallets
==============

A **Key** is an object that provides an abstraction for the agency of signing transactions.

Key (abstract)
--------------

Implementers of Keys meant for signing should override the following methods:

Key.sign()<terra_sdk.key.key.Key.sign>
Key.create_signature()<terra_sdk.key.key.Key.create_signature> 



.. automodule:: class Key:
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


RawKey
------
RawKey directly uses a raw (plaintext) private key in memory, and provides the implementation for signing with ECDSA on curve Secp256k1

.. automodule:: class RawKey(Key):

    Args:
        private_key (bytes): private key in bytes
    """

    private_key: bytes
    """Private key, in bytes."""
    




MnemonicKey
-----------
A MnemonicKey derives a private key using a BIP39 mnemonic seed phrase, and provides key-derivation options based on the BIP44 HD path standard. A mnemonic is a string that is optional in the class. If not provided, a 24-word mnemonic will be generated.

.. automodule:: class MnemonicKey(RawKey):
    """
    Args:
        account (int, optional): HD path parameter - account number.
        index (int, optional): HD path parameter - account index.
        coin_type (int, optional): HD path parameter - coin type.
    """

    mnemonic: str
    """Mnemonic key phrase associated with the account (space-separated)."""

    account: int
    """HD path parameter: account number."""

    index: int
    """HD path parameter: account index."""

    coin_type: int
    """HD path parameter: coin type"""

Wallet
------

.. automodule:: terra_sdk.client.lcd.wallet
    :members:
