from ._base import BaseAPI

__all__ = ["TxAPI"]


class TxAPI(BaseAPI):
    async def tx_info(self, tx_hash: string) -> TxInfo:
        return TxInfo.from_data(await self._c._get(f"/txs/{tx_hash}", raw=True))

    async def create(
        self,
        source_address: str,
        msgs: List[Msg],
        fee: Optional[StdFee] = None,
        memo: Optional[str] = "",
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
        account_number: Optional[int] = None,
        sequence: Optional[int] = None,
    ) -> StdSignMsg:
        if fee is None:
            # create the fake fee
            balance = await self._c.bank.balance(source_address)
            balance_one = [Coin(c.denom, 1) for c in balance]

            # estimate the fee
            gas_prices = gas_prices or self._c.gas_prices
            gas_adjustment = gas_adjustment or self._c.gas_prices
            tx = StdTx(msgs, StdFee(0, balance_one), [], memo)
            fee = await self.estimate_fee(tx, gas_prices, gas_adjustment)

        if account_number is None or sequence is None:
            account = await self._c.auth.account_info(source_address)
            if account_number is None:
                account_number = account.account_number
            if sequence is None:
                sequnce = account.sequence

        return StdSignMsg(
            self._c.config.chain_id, account_number, sequence, fee, msgs, memo
        )

    async def estimate_fee(
        self,
        tx: Union[StdSignMsg, StdTx],
        gas_prices: Option[Coins.Input] = None,
        gas_adjustment: Option[Numeric.Input] = None,
    ) -> StdTx:
        gas_prices = gas_prices or self._c.gas_prices
        gas_adjustment = gas_adjustment or self._c.gas_prices

        if isinstance(tx, StdSignMsg):
            tx_value = tx.to_stdtx().to_data()["value"]
        else:
            tx_value = tx.to_data()["value"]

        tx_value["fee"]["gas"] = "0"

        data = {
            "tx": tx_value,
            "gas_prices": gas_prices and Coins(gasPrices).to_data(),
            "gas_adjustment": gas_adjustment and str(gas_adjustment),
        }

        res = await self._c._post("/txs/estimate_fee", data)
        return StdFee(int(d["gas"]), Coins.from_data(d["fees"]))

    async def encode(self, tx: StdTx) -> str:
        res = await self._c._post("/txs/encode", tx.to_data())
        return res["tx"]

    async def hash(self, tx: StdTx) -> str:
        amino = await self.encode(tx)
        return hash_amino(amino)

    async def _broadcast(self, tx: StdTx, mode: str) -> dict:
        data = {"tx": tx.to_data().value, "mode": mode}
        return await self._c._post("/txs", data)

    async def broadcast_sync(self, tx: StdTx) -> SyncTxBroadcastResult:
        res = await self._broadcast(tx, "sync")
        return res

    async def broadcast_async(self, tx: StdTx) -> AsyncTxBroadcastResult:
        res = await self._broadcast(tx, "async")
        return res

    async def broadcast(self, tx: StdTx) -> BlockTxBroadcastResult:
        res = await self._broadcast(tx, "block")
        return res

    async def search(self, options: dict = {}) -> dict:
        res = await self._c._get("/txs", options, raw=True)
        return res
