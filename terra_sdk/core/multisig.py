"""Data objects about Multi-Signature."""

from __future__ import annotations

from typing import List

import attr

from terra_sdk.core.compact_bit_array import CompactBitArray
from terra_sdk.core.public_key import LegacyAminoMultisigPublicKey, SimplePublicKey
from terra_sdk.core.signature_v2 import Descriptor
from terra_sdk.core.signature_v2 import Multi as MultiDescriptor
from terra_sdk.core.signature_v2 import SignatureV2
from terra_sdk.util.json import JSONSerializable

__all__ = ["MultiSignature"]


@attr.s
class MultiSignature(JSONSerializable):
    bitarray: CompactBitArray = attr.ib(init=False)
    signatures: List[Descriptor] = attr.ib(init=False)
    multisig_pubkey: LegacyAminoMultisigPublicKey = attr.ib()

    def __attrs_post_init__(self):
        n = len(self.multisig_pubkey.public_keys)
        self.bitarray = CompactBitArray.from_bits(n)
        self.signatures = []

    def append_signature(self, signature_data: Descriptor, index: int):
        new_idx = self.bitarray.num_true_bits_before(index)

        # in case of signature already exists, just replace
        if self.bitarray.get_index(index):
            self.signatures[new_idx] = signature_data
            return

        self.bitarray.set_index(index, True)
        # optimization
        if new_idx == len(self.signatures):
            self.signatures.append(signature_data)
            return

        self.signatures.insert(new_idx, signature_data)

    def append_signature_from_pubkey(
        self, signature_data: Descriptor, public_key: SimplePublicKey
    ):
        index = 0
        for i, v in enumerate(self.multisig_pubkey.public_keys):
            if v.key == public_key.key:
                index = i
                break
        if index < 0:
            raise ValueError("provided key doesn't exist in public_keys")
        self.append_signature(signature_data, index)

    def append_signature_v2s(self, signatures: List[SignatureV2]):
        for sig in signatures:
            if not isinstance(sig.public_key, SimplePublicKey):
                raise ValueError("non-SimplePublicKey cannot be used to sign multisig")
            self.append_signature_from_pubkey(sig.data, sig.public_key)

    def to_signature_descriptor(self) -> Descriptor:
        return Descriptor(
            multi=MultiDescriptor(bitarray=self.bitarray, signatures=self.signatures)
        )
