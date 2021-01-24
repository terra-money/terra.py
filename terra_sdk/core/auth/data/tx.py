from __future__ import annotations
from terra_sdk.core.public_key import PublicKey
from terra_sdk.core.coins import Coins

import attr


@attr.s
class StdSignature:

    signature: str = attr.ib()
    pub_key: PublicKey = attr.ib()

    def to_data(self) -> dict:
        return {"signature": self.signature, "pub_key": self.pub_key}

    @classmethod
    def from_data(cls, data: dict) -> StdSignature:
        return cls(
            signature=data.get("signature"),
            pub_key=PublicKey.from_data(data.get("pub_key")),
        )


@attr.s
class StdFee:

    gas: int = attr.ib()
    amount: Coins = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> StdFee:
        return cls(int(data["gas"]), Coins.from_data(data["amount"]))

    def to_data(self) -> dict:
        return {"gas": str(self.gas), "amount": self.amount.to_data()}

    @property
    def gas_prices(self) -> Coins:
        return self.amount.to_dec_coins().div(self.gas)


@attr.s
class StdSignMsg:

    chain_id: str = attr.ib()
    account_number: int = attr.ib()
    sequence: int = attr.ib()
    fee: StdFee = attr.ib()
    msgs: List[Msg] = attr.ib()
    memo: str = attr.ib()

    def to_stdtx(self) -> StdTx:
        return StdTx(self.msgs, self.fee, [], self.memo)

    def to_data(self) -> dict:
        return {
            "chain_id": self.chain_id,
            "account_number": str(self.account_number),
            "sequence": str(self.sequence),
            "fee": self.fee.to_data(),
            "msgs": [m.to_data() for m in self.msgs],
            "memo": self.memo,
        }

    @classmethod
    def from_data(cls, data: dict) -> StdSignMsg:
        return cls(
            data["chain_id"],
            int(data["account_number"]),
            int(data["sequence"]),
            StdFee.from_data(data["fee"]),
            [Msg.from_data(m) for m in data["msgs"]],
            data["memo"],
        )


@attr.s
class StdTx:

    msg: List[StdMsg] = attr.ib()
    fee: StdFee = attr.ib()
    signatures: List[StdSignature] = attr.ib()
    memo: str = attr.ib()

    def to_data(self) -> dict:
        return {
            "type": "core/StdTx",
            "value": {
                "msg": [m.to_data() for m in self.msg],
                "fee": self.fee.to_data(),
                "signatures": [s.to_data() for s in self.signatures],
                "memo": self.memo,
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> StdTx:
        data = data["value"]
        return cls(
            [Msg.from_data(m) for m in data["msg"]],
            StdFee.from_data(data["fee"]),
            [StdSignature.from_data(s) for s in data["signatures"]],
            data["memo"],
        )


@attr.s
class TxInfo:

    height: int = attr.ib()
    txhash: str = attr.ib()
    rawlog: string = attr.ib()
    logs: Optional[List[TxLog]] = attr.ib()
    gas_wanted: int = attr.ib()
    gas_used: int = attr.ib()
    timestamp: str = attr.ib()
    code: Optional[int] = attr.ib()
    codespace: Optional[int] = attr.ib()

    def to_data(self) -> dict:
        data = {
            "height": str(self.height),
            "txhash": self.txhash,
            "raw_log": self.rawlog,
            "gas_wanted": str(self.gas_wanted),
            "gas_used": str(self.gas_used),
            "timestamp": self.timestamp,
            "tx": self.tx.to_data(),
        }

        if self.logs:
            data["logs"] = [l.to_data() for l in log]

        if self.code:
            data["code"] = self.code

        if self.codespace:
            data["codespace"] = self.codespace

        return data

    @classmethod
    def from_data(cls, data: dict) -> TxInfo:
        return cls(
            int(data["height"]),
            data["txhash"],
            data["raw_log"],
            [TxLog.from_data(l) for l in data.get("logs")],
            int(data["gas_wanted"]),
            int(data["gas_used"]),
            StdTx.from_data(data["tx"]),
            data["timestamp"],
            data.get("code"),
            data.get("codespace"),
        )