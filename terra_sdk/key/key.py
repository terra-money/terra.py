import abc
import base64
import copy
import hashlib
from typing import Optional

import attr
from bech32 import bech32_encode, convertbits

from terra_sdk.core import (
    AccAddress,
    AccPubKey,
    SignatureV2,
    SignDoc,
    ValAddress,
    ValPubKey,
)
from terra_sdk.core.public_key import PublicKey, get_bech, address_from_public_key, pubkey_from_public_key
from terra_sdk.core.signature_v2 import Descriptor
from terra_sdk.core.signature_v2 import Single as SingleDescriptor
from terra_sdk.core.tx import ModeInfo, ModeInfoSingle, SignerInfo, SignMode, Tx

from terra_sdk.core.public_key import (
    BECH32_AMINO_PUBKEY_DATA_PREFIX_SECP256K1,
    BECH32_AMINO_PUBKEY_DATA_PREFIX_ED25519,
    BECH32_AMINO_PUBKEY_DATA_PREFIX_MULTISIG_THRESHOLD
)


__all__ = ["Key", "SignOptions"]


@attr.s
class SignOptions:
    account_number: int = attr.ib(converter=int)
    sequence: int = attr.ib(converter=int)
    sign_mode: SignMode = attr.ib()
    chain_id: str = attr.ib()


class Key:
    """Abstract Key interface, representing an agent with transaction-signing capabilities.

    Args:
        public_key (Optional[bytes]): compressed public key bytes,
    """

    public_key: Optional[PublicKey]
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

    def create_signature_amino(self, signDoc: SignDoc) -> SignatureV2:
        if self.public_key is None:
            raise ValueError(
                "signature could not be created: Key instance missing public_key"
            )

        return SignatureV2(
            public_key=self.public_key,
            data=Descriptor(
                SingleDescriptor(
                    mode=SignMode.SIGN_MODE_LEGACY_AMINO_JSON,
                    signature=(self.sign(signDoc.to_amino_json())),
                )
            ),
            sequence=signDoc.sequence,
        )

    def create_signature(self, signDoc: SignDoc) -> SignatureV2:
        """Signs the transaction with the signing algorithm provided by this Key implementation,
        and outputs the signature. The signature is only returned, and must be manually added to
        the ``signatures`` field of an :class:`Tx`.

        Args:
            signDoc (SignDoc): unsigned transaction

        Raises:
            ValueError: if missing ``public_key``

        Returns:
            SignatureV2: signature object
        """
        if self.public_key is None:
            raise ValueError(
                "signature could not be created: Key instance missing public_key"
            )

        # make backup
        si_backup = copy.deepcopy(signDoc.auth_info.signer_infos)
        signDoc.auth_info.signer_infos = [
            SignerInfo(
                public_key=self.public_key,
                sequence=signDoc.sequence,
                mode_info=ModeInfo(
                    single=ModeInfoSingle(mode=SignMode.SIGN_MODE_DIRECT)
                ),
            )
        ]
        signature = self.sign(signDoc.to_bytes())

        # restore
        signDoc.auth_info.signer_infos = si_backup

        return SignatureV2(
            public_key=self.public_key,
            data=Descriptor(
                single=SingleDescriptor(
                    mode=SignMode.SIGN_MODE_DIRECT, signature=signature
                )
            ),
            sequence=signDoc.sequence,
        )

    def sign_tx(self, tx: Tx, options: SignOptions) -> Tx:
        """Signs the transaction with the signing algorithm provided by this Key implementation,
        and creates a ready-to-broadcast :class:`Tx` object with the signature applied.

        Args:
            tx (Tx): unsigned transaction
            options (SignOptions): options for signing

        Returns:
            Tx: ready-to-broadcast transaction object
        """

        signedTx = copy.deepcopy(tx)
        signDoc = SignDoc(
            chain_id=options.chain_id,
            account_number=options.account_number,
            sequence=options.sequence,
            auth_info=signedTx.auth_info,
            tx_body=signedTx.body,
        )

        if options.sign_mode == SignMode.SIGN_MODE_LEGACY_AMINO_JSON:
            signature: SignatureV2 = self.create_signature_amino(signDoc)
        else:
            signature: SignatureV2 = self.create_signature(signDoc)

        sigData: SingleDescriptor = signature.data.single
        for sig in tx.signatures:
            signedTx.signatures.append(sig)
        signedTx.signatures.append(sigData.signature)
        for infos in tx.auth_info.signer_infos:
            signedTx.auth_info.signer_infos.append(infos)
        signedTx.auth_info.signer_infos.append(
            SignerInfo(
                public_key=signature.public_key,
                sequence=signature.sequence,
                mode_info=ModeInfo(single=ModeInfoSingle(mode=sigData.mode)),
            )
        )
        return signedTx
