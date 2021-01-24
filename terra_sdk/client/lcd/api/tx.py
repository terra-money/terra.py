from ._base import BaseAPI

__all__ = ["TxAPI"]


class TxAPI(BaseAPI):
    async def tx_info(self, tx_hash: string) -> TxInfo:
        return TxInfo.from_data(await self._c._get(f"/txs/{tx_hash}", raw=True))

    async def create(self, source_address: str, **options) -> StdSignMsg:
        pass

    async def estimate_fee(
        self, tx: Union[StdSignMsg, StdTx], gas_prices=None, gas_adjustment=None
    ):
        pass

    async def encode(self, tx: StdTx) -> str:
        pass

    async def hash(self, tx: StdTx) -> str:
        pass
