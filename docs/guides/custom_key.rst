.. keys:

Implementing a Custom Key
=========================

If none of the Key solutions provided by Terra SDK or the community are able to meet your requirements, 
you might consider writing your own Key implementation. 

Here are just a couple  that help guide
your design pathways:

Is the private key accessible by developer?
    * YES: Subclass :class:`terra_sdk.key.raw.RawKey`
    * NO: Subclass :class:`terra_sdk.key.key.Key`

Can the signing agent sign arbitrary data payloads AND use ECDSA on Secp256k1?
    * YES: Override :meth:`Key.sign()<terra_sdk.key.key.Key.sign>`
    * NO: Override :meth:`Key.create_signature()<terra_sdk.key.key.Key.create_signature>`

Can you determine the public key in advance, and is it static?
    * YES: Call ``super()`` in constructor with public key to generate addresses & pubkeys
    * NO: Override :meth:`acc_address<terra_sdk.key.key.Key.acc_address>`, :meth:`val_address<terra_sdk.key.key.Key.val_address>`, :meth:`acc_pubkey<terra_sdk.key.key.Key.acc_pubkey>`, :meth:`val_pubkey<terra_sdk.key.key.Key.val_pubkey>` properties.


Usually, reasons for requiring a custom Key fall into one of 3 patterns:

* External signing

    **Scenario:** The transaction signing is to be performed outside the Python program running Terra SDK,
    such as signing via hardware wallet (Ledger, Trezor), etc. 


* Alternative signing algorithm

    **Scenario:** Terra account you need to sign transactions for requires a signature algorithm other than
    ECDSA on Secp256k1, such as Threshold Multisig or Ed25519. 


* Customize private key derivation

    **Scenario:** User wants to provide a custom interface for generating a private key, eg. alternative mnemonic schemas,
    directed key.

The source for MnemonicKey is provided as an example:

.. code-block:: python

    from terra_sdk.key.raw import RawKey
    from bip32utils import BIP32_HARDEN, BIP32Key
    from mnemonic import Mnemonic

    class MnemonicKey(RawKey):
        def __init__(
            self,
            mnemonic: str = None,
            account: int = 0,
            index: int = 0,
            coin_type: int = 330,
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
