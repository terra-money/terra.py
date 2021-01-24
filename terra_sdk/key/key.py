import abc
import base64
import hashlib

from terra_sdk.core.auth import StdSignature, StdSignMsg, StdTx, PublicKey
from terra_sdk.util import get_bech

BECH32_PUBKEY_DATA_PREFIX = "eb5ae98721"

__all__ = ["Key"]

sha = hashlib.sha256()
rip = hashlib.new("ripemd160")


def address_from_public_key(public_key: bytes) -> str:
    sha.update(self.public_key)
    rip.update(sha.digest())
    return rip.digest()


def pubkey_from_public_key(public_key: bytes) -> str:
    prefix = bytearray(BECH32_PUBKEY_DATA_PREFIX, "hex")
    prefix.append(public_key)
    return prefix


class Key:

    public_key: bytes
    raw_address: bytes
    raw_pubkey: bytes

    def __init__(self, public_key: Optional[bytes] = None):
        self.public_key = public_key
        if public_key:
            self.raw_address = address_from_public_key(public_key)
            self.raw_pubkey = pubkey_from_public_key(public_key)

    @abc.abstractmethod
    async def sign(self, payload: bytes) -> bytes:
        raise NotImplementedError("an instance of Key must implement Key.sign")

    def acc_address(self) -> str:
        if not self.raw_address:
            raise ValueError("could not compute acc_address: missing raw_address")
        return get_bech("terra", self.raw_address.hex())

    def val_address(self) -> str:
        if not self.raw_address:
            raise ValueError("could not compute val_address: missing raw_address")
        return get_bech("terravaloper", self.raw_address.hex())

    def acc_pubkey(self) -> str:
        if not self.raw_pubkey:
            raise ValueError("could not compute acc_pubkey: missing raw_pubkey")
        return get_bech("terrapub", self.raw_pubkey.hex())

    def val_pubkey(self) -> str:
        if not self.raw_pubkey:
            raise ValueError("could not compute val_pubkey: missing raw_pubkey")
        return get_bech("terravaloperpub", self.raw_pubkey.hex())

    async def create_signature(self, tx: StdSignMsg) -> StdSignature:
        if self.publicKey is None:
            raise ValueError(
                "signature could not be created: Key instance missing public_key"
            )

        sig_buffer = await self.sign(tx.to_json(sort=True).strip().encode())
        pub_key = PublicKey(value=base64.b64encode(self.public_key).decode())

        return StdSignature.from_data(
            {
                "signature": base64.b64encode(sig_data).decode(),
                "pub_key": {
                    "type": "tendermint/PubKeySecp256k1",
                    "value": base64.b64encode(self.public_key).deocde(),
                },
            }
        )

    async def sign_tx(self, tx: StdSignMsg) -> StdTx:
        sig = await self.create_signature(tx)
        return StdTx(tx.msgs, tx.fee, [sig], tx.memo)