"""Data objects about SignDoc."""

from __future__ import annotations

from typing import Dict, List, Optional

import attr

from terra_sdk.core import AccAddress
from terra_sdk.core.coins import Coins
from terra_sdk.core.public_key import PublicKey
from terra_sdk.core.tx import AuthInfo, TxBody
from terra_sdk.util.json import JSONSerializable

from terra_proto.cosmos.tx.v1beta1 import SignDoc as SignDoc_pb
from terra_proto.cosmos.tx.v1beta1 import TxBody as TxBody_pb

__all__ = ["SignDoc"]

class SignDoc(JSONSerializable, SignDoc_pb):

    __doc__ == SignDoc_pb.__doc__

    tx_body: TxBody_pb

    @classmethod
    def from_data(cls, data: dict) -> SignDoc:
        data = data["value"]
        return cls(
            chain_id=data["chain_id"],
            account_number=data["account_number"],
            sequence=data["sequence"],
            auth_info=AuthInfo.from_data(data["auth_info"]),  # FIXME: encode/base64
            tx_body=TxBody.from_data(data["tx_body"]) # FIXME: encode/base64)
        )

    def to_data(self) -> dict:
        self.to_json()
        return {
            "chain_id": self.chain_id,
            "account_nubmer": self.account_number,
            "sequence": self.sequence,
            "auth_info": self.auth_info.to_data(),
            "tx_body": self.tx_body.to_data()
        }
    @classmethod
    def from_proto(cls, proto: SignDoc_pb) -> SignDoc:
        return cls(
            chain_id=proto.chain_id,
            account_number=proto.account_number,
            auth_info=AuthInfo.from_proto(proto.auth_info_bytes), # FIXME: encode/base64,
            tx_body=TxBody.from_proto(proto.body_bytes)  # FIXME: encode/base64
        )

    def to_proto(self) -> SignDoc_pb:
        proto = SignDoc_pb()
        proto.chain_id = self.chain_id
        proto.account_number = self.account_number
        proto.auth_info_bytes = self.auth_info.to_proto(), # FIXME: encode/base64
        proto.body_bytes = self.tx_body.to_proto() # FIXME: encode/base64
        return proto

    def to_bytes(self) -> bytes:
        return self.to_proto().to_json().encode('base64')
