from typing import List, Optional, Union

from terra_sdk.core import AccAddress, Coin, Coins, Numeric
from terra_sdk.core.auth import StdFee, StdSignMsg, StdTx, TxInfo
from terra_sdk.core.broadcast import (
    AsyncTxBroadcastResult,
    BlockTxBroadcastResult,
    SyncTxBroadcastResult,
)
from terra_sdk.core.msg import Msg
from terra_sdk.util.hash import hash_amino

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncTxAPI", "TxAPI"]


class AsyncTxAPI(BaseAsyncAPI):
    async def tx_info(self, tx_hash: str) -> TxInfo:
        """Fetches information for an included transaction given a tx hash.

        Args:
            tx_hash (str): hash of transaction to lookup

        Returns:
            TxInfo: transaction info
        """
        return TxInfo.from_data(await self._c._get(f"/txs/{tx_hash}", raw=True))

    async def create(
        self,
        source_address: AccAddress,
        msgs: List[Msg],
        fee: Optional[StdFee] = None,
        memo: str = "",
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
        denoms: Optional[List[str]] = None,
        account_number: Optional[int] = None,
        sequence: Optional[int] = None,
    ) -> StdSignMsg:
        """Create a new unsigned transaction, with helpful utilities such as lookup of
        chain ID, account number, sequence and fee estimation.

        Args:
            source_address (AccAddress): transaction sender's account address
            msgs (List[Msg]): list of messages to include
            fee (Optional[StdFee], optional): fee to use (estimates if empty).
            memo (str, optional): memo to use. Defaults to "".
            gas_prices (Optional[Coins.Input], optional): gas prices for fee estimation.
            gas_adjustment (Optional[Numeric.Input], optional): gas adjustment for fee estimation.
            denoms (Optional[List[str]], optional): list of denoms to use for gas fee when estimating.
            account_number (Optional[int], optional): account number to use.
            sequence (Optional[int], optional): sequence number to use.

        Returns:
            StdSignMsg: unsigned tx
        """
        if fee is None:

            # create the fake fee
            balance = await BaseAsyncAPI._try_await(
                self._c.bank.balance(source_address)
            )
            balance_one = [Coin(c.denom, 1) for c in balance]

            # estimate the fee
            tx = StdTx(msgs, StdFee(0, balance_one), [], memo)
            fee = await BaseAsyncAPI._try_await(
                self.estimate_fee(tx, gas_prices, gas_adjustment, denoms)
            )

        if account_number is None or sequence is None:
            account = await BaseAsyncAPI._try_await(
                self._c.auth.account_info(source_address)
            )
            if account_number is None:
                account_number = account.account_number
            if sequence is None:
                sequence = account.sequence

        return StdSignMsg(
            self._c.chain_id, account_number or 0, sequence or 0, fee, msgs, memo  # type: ignore
        )

    async def estimate_fee(
        self,
        tx: Union[StdSignMsg, StdTx],
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
        denoms: Optional[List[str]] = None,
    ) -> StdFee:
        """Estimates the proper fee to apply by simulating it within the node.

        Args:
            tx (Union[StdSignMsg, StdTx]): transaction to estimate fee for
            gas_prices (Optional[Coins.Input], optional): gas prices to use.
            gas_adjustment (Optional[Numeric.Input], optional): gas adjustment to use.
            denoms (Optional[List[str]], optional): list of denoms to use to pay for gas.

        Returns:
            StdFee: estimated fee
        """
        gas_prices = gas_prices or self._c.gas_prices
        gas_adjustment = gas_adjustment or self._c.gas_adjustment

        if isinstance(tx, StdSignMsg):
            tx_value = tx.to_stdtx().to_data()["value"]
        else:
            tx_value = tx.to_data()["value"]

        tx_value["fee"]["gas"] = "0"

        data = {
            "tx": tx_value,
            "gas_prices": gas_prices and Coins(gas_prices).to_data(),
            "gas_adjustment": gas_adjustment and str(gas_adjustment),
        }

        res = await self._c._post("/txs/estimate_fee", data)
        fees = Coins.from_data(res["fees"])
        # only pick the denoms we are interested in?
        if denoms:
            fees = fees.filter(lambda c: c.denom in denoms)  # type: ignore
        return StdFee(int(res["gas"]), fees)

    async def encode(self, tx: StdTx) -> str:
        """Fetches a transaction's amino encoding.

        Args:
            tx (StdTx): transaction to encode

        Returns:
            str: base64 string containing amino-encoded tx
        """
        res = await self._c._post("/txs/encode", tx.to_data())
        return res["tx"]

    async def hash(self, tx: StdTx) -> str:
        """Compute hash for a transaction.

        Args:
            tx (StdTx): transaction to hash

        Returns:
            str: transaction hash
        """
        amino = await self.encode(tx)
        return hash_amino(amino)

    async def _broadcast(self, tx: StdTx, mode: str) -> dict:
        data = {"tx": tx.to_data()["value"], "mode": mode}
        return await self._c._post("/txs", data, raw=True)

    async def broadcast_sync(self, tx: StdTx) -> SyncTxBroadcastResult:
        """Broadcasts a transaction using the ``sync`` broadcast mode.

        Args:
            tx (StdTx): transaction to broadcast

        Returns:
            SyncTxBroadcastResult: result
        """
        res = await self._broadcast(tx, "sync")
        return SyncTxBroadcastResult(
            height=res["height"],
            txhash=res["txhash"],
            raw_log=res["raw_log"],
            code=res.get("code"),
            codespace=res.get("codespace"),
        )

    async def broadcast_async(self, tx: StdTx) -> AsyncTxBroadcastResult:
        """Broadcasts a transaction using the ``async`` broadcast mode.

        Args:
            tx (StdTx): transaction to broadcast

        Returns:
            AsyncTxBroadcastResult: result
        """
        res = await self._broadcast(tx, "async")
        return AsyncTxBroadcastResult(
            height=res["height"],
            txhash=res["txhash"],
        )

    async def broadcast(self, tx: StdTx) -> BlockTxBroadcastResult:
        """Broadcasts a transaction using the ``block`` broadcast mode.

        Args:
            tx (StdTx): transaction to broadcast

        Returns:
            BlockTxBroadcastResult: result
        """
        res = await self._broadcast(tx, "block")
        return BlockTxBroadcastResult(
            height=res["height"],
            txhash=res["txhash"],
            raw_log=res["raw_log"],
            gas_wanted=res["gas_wanted"],
            gas_used=res["gas_used"],
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
        res = await self._c._get("/txs", options, raw=True)
        return res


class TxAPI(AsyncTxAPI):
    @sync_bind(AsyncTxAPI.tx_info)
    def tx_info(self, tx_hash: str) -> TxInfo:
        pass

    tx_info.__doc__ = AsyncTxAPI.tx_info.__doc__

    @sync_bind(AsyncTxAPI.create)
    def create(
        self,
        source_address: AccAddress,
        msgs: List[Msg],
        fee: Optional[StdFee] = None,
        memo: str = "",
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
        denoms: Optional[List[str]] = None,
        account_number: Optional[int] = None,
        sequence: Optional[int] = None,
    ) -> StdSignMsg:
        pass

    create.__doc__ = AsyncTxAPI.create.__doc__

    @sync_bind(AsyncTxAPI.estimate_fee)
    def estimate_fee(
        self,
        tx: Union[StdSignMsg, StdTx],
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
        denoms: Optional[List[str]] = None,
    ) -> StdFee:
        pass

    estimate_fee.__doc__ = AsyncTxAPI.estimate_fee.__doc__

    @sync_bind(AsyncTxAPI.encode)
    def encode(self, tx: StdTx) -> str:
        pass

    encode.__doc__ = AsyncTxAPI.encode.__doc__

    @sync_bind(AsyncTxAPI.hash)
    def hash(self, tx: StdTx) -> str:
        pass

    hash.__doc__ = AsyncTxAPI.hash.__doc__

    @sync_bind(AsyncTxAPI.broadcast_sync)
    def broadcast_sync(self, tx: StdTx) -> SyncTxBroadcastResult:
        pass

    broadcast_sync.__doc__ = AsyncTxAPI.broadcast_sync.__doc__

    @sync_bind(AsyncTxAPI.broadcast_async)
    def broadcast_async(self, tx: StdTx) -> AsyncTxBroadcastResult:
        pass

    broadcast_async.__doc__ = AsyncTxAPI.broadcast_async.__doc__

    @sync_bind(AsyncTxAPI.broadcast)
    def broadcast(self, tx: StdTx) -> BlockTxBroadcastResult:
        pass

    broadcast.__doc__ = AsyncTxAPI.broadcast.__doc__

    @sync_bind(AsyncTxAPI.search)
    def search(self, options: dict = {}) -> dict:
        pass

    search.__doc__ = AsyncTxAPI.search.__doc__
