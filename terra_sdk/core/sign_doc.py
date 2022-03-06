"""Data objects about SignDoc."""

from __future__ import annotations

import json

import attr
from terra_proto.cosmos.tx.v1beta1 import SignDoc as SignDoc_pb

from terra_sdk.core.tx import AuthInfo, TxBody
from terra_sdk.util.json import JSONSerializable

__all__ = ["SignDoc"]

from terra_sdk.util.remove_none import remove_none


@attr.s
class SignDoc(JSONSerializable):
    chain_id: str = attr.ib()
    account_number: int = attr.ib(converter=int)
    sequence: int = attr.ib(converter=int)
    auth_info: AuthInfo = attr.ib()
    tx_body: TxBody = attr.ib()

    def to_amino(self) -> dict:
        tx = self.tx_body
        auth = self.auth_info
        return {
            "chain_id": self.chain_id,
            "account_number": str(self.account_number),
            "sequence": str(self.sequence),
            "timeout_height": str(tx.timeout_height)
            if (tx.timeout_height is not None and tx.timeout_height != 0)
            else None,
            "fee": auth.fee.to_amino(),
            "msgs": [msg.to_amino() for msg in tx.messages],
            "memo": tx.memo if tx.memo else "",
        }

    @classmethod
    def from_data(cls, data: dict) -> SignDoc:
        return cls(
            chain_id=data["chain_id"],
            account_number=data["account_number"],
            sequence=data["sequence"],
            auth_info=AuthInfo.from_data(data["auth_info"]),
            tx_body=TxBody.from_data(data["tx_body"]),
        )

    def to_data(self) -> dict:
        return {
            "chain_id": self.chain_id,
            "account_nubmer": self.account_number,
            "sequence": self.sequence,
            "auth_info": self.auth_info.to_data(),
            "tx_body": self.tx_body.to_data(),
        }

    @classmethod
    def from_proto(cls, proto: SignDoc_pb) -> SignDoc:
        return cls(
            chain_id=proto.chain_id,
            account_number=proto.account_number,
            auth_info=AuthInfo.from_proto(proto.auth_info_bytes),
            tx_body=TxBody.from_proto(proto.body_bytes),
        )

    def to_proto(self) -> SignDoc_pb:
        return SignDoc_pb(
            body_bytes=bytes(self.tx_body.to_proto()),
            auth_info_bytes=bytes(self.auth_info.to_proto()),
            chain_id=self.chain_id,
            account_number=self.account_number,
        )

    def to_bytes(self) -> bytes:
        return bytes(self.to_proto())

    def to_amino_json(self) -> bytes:
        amino = self.to_amino()
        return bytes(
            json.dumps(remove_none(amino), sort_keys=True, separators=(",", ":")),
            "utf-8",
        )
