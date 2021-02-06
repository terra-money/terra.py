from terra_sdk.core import Coin, Coins, Dec

from ._base import BaseAPI


class AsyncTreasuryAPI(BaseAPI):
    async def tax_cap(self, denom: str) -> Coin:
        res = await self._c._get(f"/treasury/tax_cap/{denom}")
        return Coin(denom, res)

    async def tax_rate(self) -> Dec:
        res = await self._c._get("/treasury/tax_rate")
        return Dec(res)

    async def reward_weight(self) -> Dec:
        res = await self._c._get("/treasury/reward_weight")
        return Dec(res)

    async def tax_proceeds(self) -> Coins:
        res = await self._c._get("/treasury/tax_proceeds")
        return Coins.from_data(res)

    async def seigniorage_proceeds(self) -> Coin:
        res = await self._c._get("/treasury/seigniorage_proceeds")
        return Coin("uluna", res)

    async def parameters(self) -> Coin:
        res = await self._c._get("/treasury/parameters")
        return res


class TreasuryAPI(BaseAPI):
    def tax_cap(self, denom: str) -> Coin:
        res = self._c._get(f"/treasury/tax_cap/{denom}")
        return Coin(denom, res)

    def tax_rate(self) -> Dec:
        res = self._c._get("/treasury/tax_rate")
        return Dec(res)

    def reward_weight(self) -> Dec:
        res = self._c._get("/treasury/reward_weight")
        return Dec(res)

    def tax_proceeds(self) -> Coins:
        res = self._c._get("/treasury/tax_proceeds")
        return Coins.from_data(res)

    def seigniorage_proceeds(self) -> Coin:
        res = self._c._get("/treasury/seigniorage_proceeds")
        return Coin("uluna", res)

    def parameters(self) -> Coin:
        res = self._c._get("/treasury/parameters")
        return res
