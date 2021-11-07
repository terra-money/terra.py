import base64
import copy
from typing import List, Optional

import attr
from terra_proto.cosmos.tx.v1beta1 import SimulateResponse as SimulateResponse_pb

from terra_sdk.core import AccAddress, Coins, Dec, Numeric, PublicKey
from terra_sdk.core.broadcast import (
    AsyncTxBroadcastResult,
    BlockTxBroadcastResult,
    SyncTxBroadcastResult,
)
from terra_sdk.core.msg import Msg
from terra_sdk.core.tx import AuthInfo, Fee, SignerData, SignMode, Tx, TxBody, TxInfo
from terra_sdk.util.hash import hash_amino
from terra_sdk.util.json import JSONSerializable

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncTxAPI", "TxAPI", "BroadcastOptions", "CreateTxOptions"]


@attr.s
class SignerOptions:
    address: str = attr.ib()
    sequence: Optional[int] = attr.ib(default=None)
    public_key: Optional[PublicKey] = attr.ib(default=None)


@attr.s
class CreateTxOptions:
    msgs: List[Msg] = attr.ib()
    fee: Optional[Fee] = attr.ib(default=None)
    memo: Optional[str] = attr.ib(default=None)
    gas: Optional[str] = attr.ib(default=None)
    gas_prices: Optional[Coins] = attr.ib(default=None)
    # FIXME: is it okay with 0 bye default?
    gas_adjustment: Optional[Numeric.Output] = attr.ib(
        default=0, converter=Numeric.parse
    )
    fee_denoms: Optional[str] = attr.ib(default=None)
    account_number: Optional[int] = attr.ib(default=None)
    sequence: Optional[int] = attr.ib(default=None)
    timeout_height: Optional[int] = attr.ib(default=None)
    sign_mode: Optional[SignMode] = attr.ib(default=None)


@attr.s
class BroadcastOptions:
    sequences: Optional[List[int]] = attr.ib()
    fee_granter: Optional[AccAddress] = attr.ib(default=None)


@attr.s
class GasInfo:
    gas_wanted: int = attr.ib(converter=int)
    gas_used: int = attr.ib(converter=int)


@attr.s
class EventAttribute:
    key: str = attr.ib()
    value: str = attr.ib()


@attr.s
class Event:
    type: str = attr.ib()
    attributes: List[EventAttribute] = attr.ib(converter=list)


@attr.s
class SimulateResult:
    data: str = attr.ib()
    log: str = attr.ib()
    events: List[Event] = attr.ib(converter=list)


@attr.s
class SimulateResponse(JSONSerializable):
    gas_info: GasInfo = attr.ib()
    result: SimulateResult = attr.ib()

    @classmethod
    def from_data(cls, data: dict):
        return cls(gas_info=data["gas_info"], result=data["result"])


class AsyncTxAPI(BaseAsyncAPI):
    async def tx_info(self, tx_hash: str) -> Tx:
        """Fetches information for an included transaction given a tx hash.

        Args:
            tx_hash (str): hash of transaction to lookup

        Returns:
            TxInfo: transaction info
        """
        res = await self._c._get(f"/cosmos/tx/v1beta1/txs/{tx_hash}")
        return TxInfo.from_data(res)

    async def create(
        self, signers: List[SignerOptions], options: CreateTxOptions
    ) -> Tx:
        """Create a new unsigned transaction, with helpful utilities such as lookup of
        chain ID, account number, sequence and fee estimation.

        Args:
            sender (AccAddress): transaction sender's account address
            msgs (List[Msg]): list of messages to include
            fee (Optional[Fee], optional): fee to use (estimates if empty).
            memo (str, optional): memo to use. Defaults to "".
            gas_prices (Optional[Coins.Input], optional): gas prices for fee estimation.
            gas_adjustment (Optional[Numeric.Input], optional): gas adjustment for fee estimation.
            fee_denoms (Optional[List[str]], optional): list of denoms to use for gas fee when estimating.
            account_number (Optional[int], optional): account number to use.
            sequence (Optional[int], optional): sequence number to use.

        Returns:
            Tx: unsigned tx
        """

        opt = copy.deepcopy(options)

        signerData: List[SignerData] = []
        for signer in signers:
            seq = signer.sequence
            pubkey = signer.public_key

            if seq is None or pubkey is None:
                acc = await BaseAsyncAPI._try_await(
                    self._c.auth.account_info(signer.address)
                )
                if seq is None:
                    seq = acc.get_sequence()
                if pubkey is None:
                    pubkey = acc.get_pubkey()
            signerData.append(SignerData(seq, pubkey))

        # create the fake fee
        if opt.fee is None:
            opt.fee = await BaseAsyncAPI._try_await(self.estimate_fee(signerData, opt))

        return Tx(
            TxBody(opt.msgs, opt.memo or "", opt.timeout_height or 0),
            AuthInfo([], opt.fee),
            "",
        )

    async def estimate_fee(
        self, signers: List[SignerOptions], options: CreateTxOptions
    ) -> Fee:
        """Estimates the proper fee to apply by simulating it within the node.

        Args:
            signers ([SignerOptions]): signers
            options (CreateTxOptions): transaction info to estimate fee

        Returns:
            Fee: estimated fee
        """

        gas_prices = options.gas_prices or self._c.gas_prices
        gas_adjustment = options.gas_adjustment or self._c.gas_adjustment

        gas_prices_coins = None
        if gas_prices:
            gas_prices_coins = Coins(gas_prices)
            if options.fee_denoms:
                _fee_denoms: List[
                    str
                ] = options.fee_denoms  # satisfy mypy type checking :(
                gas_prices_coins = gas_prices_coins.filter(
                    lambda c: c.denom in _fee_denoms
                )
        tx_body = TxBody(messages=options.msgs, memo=options.memo or "")
        emptyCoins = Coins()
        emptyFee = Fee(0, emptyCoins)
        auth_info = AuthInfo([], emptyFee)

        tx = Tx(tx_body, auth_info, [])
        tx.append_empty_signatures(signers)

        gas = options.gas
        if gas is None or gas == "auto" or gas == 0:
            opt = copy.deepcopy(options)
            opt.gas_adjustment = gas_adjustment
            gas = str(self.estimate_gas(tx, opt))

        tax_amount = self.compute_tax(tx)
        fee_amount = (
            tax_amount.add(gas_prices_coins.mul(gas).to_int_coins())
            if gas_prices_coins
            else tax_amount
        )

        return Fee(Numeric.parse(gas), fee_amount, "", "")

    async def estimate_gas(self, tx: Tx, options: Optional[CreateTxOptions]) -> int:
        gas_adjustment = options.gas_adjustment if options else self._c.gas_adjustment

        res = await self._c._post(
            "/cosmos/tx/v1beta1/simulate", {"tx_bytes": self.encode(tx)}
        )
        simulated = SimulateResponse.from_data(res)

        return int(Dec(gas_adjustment).mul(simulated.gas_info["gas_used"]))

    async def compute_tax(self, tx: Tx) -> Coins:
        res = await self._c._post(
            "/terra/tx/v1beta1/compute_tax", {"tx_bytes": self.encode(tx)}
        )
        return Coins.from_data(res.get("tax_amount"))

    async def encode(self, tx: Tx, options: BroadcastOptions = None) -> str:
        return base64.b64encode(tx.to_proto().SerializeToString()).decode()

    async def hash(self, tx: Tx) -> str:
        """Compute hash for a transaction.

        Args:
            tx (Tx): transaction to hash

        Returns:
            str: transaction hash
        """
        amino = await self.encode(tx)
        return hash_amino(amino)

    async def _broadcast(
        self, tx: Tx, mode: str, options: BroadcastOptions = None
    ) -> dict:
        data = {"tx_bytes": self.encode(tx), "mode": mode}
        return await self._c._post("/cosmos/tx/v1beta1/txs", data)  # , raw=True)

    async def broadcast_sync(
        self, tx: Tx, options: BroadcastOptions = None
    ) -> SyncTxBroadcastResult:
        """Broadcasts a transaction using the ``sync`` broadcast mode.

        Args:
            tx (Tx): transaction to broadcast
            options (BroadcastOptions): broacast options, optional

        Returns:
            SyncTxBroadcastResult: result
        """
        res = await self._broadcast(tx, "BROADCAST_MODE_SYNC", options)
        return SyncTxBroadcastResult(
            txhash=res.get("txhash"),
            raw_log=res.get("raw_log"),
            code=res.get("code"),
            codespace=res.get("codespace"),
        )

    async def broadcast_async(
        self, tx: Tx, options: BroadcastOptions = None
    ) -> AsyncTxBroadcastResult:
        """Broadcasts a transaction using the ``async`` broadcast mode.

        Args:
            tx (Tx): transaction to broadcast
            options (BroadcastOptions): broacast options, optional

        Returns:
            AsyncTxBroadcastResult: result
        """
        res = await self._broadcast(tx, "BROADCAST_MODE_ASYNC", options)
        return AsyncTxBroadcastResult(
            txhash=res.get("txhash"),
        )

    async def broadcast(
        self, tx: Tx, options: BroadcastOptions = None
    ) -> BlockTxBroadcastResult:
        """Broadcasts a transaction using the ``block`` broadcast mode.

        Args:
            tx (Tx): transaction to broadcast
            options (BroadcastOptions): broacast options, optional

        Returns:
            BlockTxBroadcastResult: result
        """
        res = await self._broadcast(tx, "BROADCAST_MODE_BLOCK", options)
        res = res["tx_response"]
        return BlockTxBroadcastResult(
            height=res.get("height") or 0,
            txhash=res.get("txhash"),
            raw_log=res.get("raw_log"),
            gas_wanted=res.get("gas_wanted") or 0,
            gas_used=res.get("gas_used") or 0,
            logs=res.get("logs"),
            code=res.get("code"),
            codespace=res.get("codespace"),
        )

    async def search(self, options: dict = {}) -> dict:
        """Searches for transactions given critera.

        Args:
            options (dict, optional): dictionary containing options. Defaults to {}.

        Returns:
            dict: transaction search results
        """
        res = await self._c._get("/cosmos/tx/v1beta1/txs", options, raw=True)
        return res


class TxAPI(AsyncTxAPI):
    @sync_bind(AsyncTxAPI.tx_info)
    def tx_info(self, tx_hash: str) -> TxInfo:
        pass

    tx_info.__doc__ = AsyncTxAPI.tx_info.__doc__

    @sync_bind(AsyncTxAPI.create)
    def create(self, signers: List[SignerOptions], options: CreateTxOptions) -> Tx:
        pass

    create.__doc__ = AsyncTxAPI.create.__doc__

    @sync_bind(AsyncTxAPI.estimate_fee)
    def estimate_fee(
        self, signers: List[SignerOptions], options: CreateTxOptions
    ) -> Fee:
        pass

    @sync_bind(AsyncTxAPI.estimate_gas)
    def estimate_gas(
        self, tx: Tx, options: Optional[CreateTxOptions]
    ) -> SimulateResponse:
        pass

    @sync_bind(AsyncTxAPI.compute_tax)
    def compute_tax(self, tx: Tx) -> Coins:
        pass

    estimate_fee.__doc__ = AsyncTxAPI.estimate_fee.__doc__

    @sync_bind(AsyncTxAPI.encode)
    def encode(self, tx: Tx, options: BroadcastOptions = None) -> str:
        pass

    encode.__doc__ = AsyncTxAPI.encode.__doc__

    @sync_bind(AsyncTxAPI.hash)
    def hash(self, tx: Tx) -> str:
        pass

    hash.__doc__ = AsyncTxAPI.hash.__doc__

    @sync_bind(AsyncTxAPI.broadcast_sync)
    def broadcast_sync(
        self, tx: Tx, options: BroadcastOptions = None
    ) -> SyncTxBroadcastResult:
        pass

    broadcast_sync.__doc__ = AsyncTxAPI.broadcast_sync.__doc__

    @sync_bind(AsyncTxAPI.broadcast_async)
    def broadcast_async(
        self, tx: Tx, options: BroadcastOptions = None
    ) -> AsyncTxBroadcastResult:
        pass

    broadcast_async.__doc__ = AsyncTxAPI.broadcast_async.__doc__

    @sync_bind(AsyncTxAPI.broadcast)
    def broadcast(
        self, tx: Tx, options: BroadcastOptions = None
    ) -> BlockTxBroadcastResult:
        pass

    broadcast.__doc__ = AsyncTxAPI.broadcast.__doc__

    @sync_bind(AsyncTxAPI.search)
    def search(self, options: dict = {}) -> dict:
        pass

    search.__doc__ = AsyncTxAPI.search.__doc__
