from terra_sdk.core import Coin, Coins, Dec

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncTreasuryAPI", "TreasuryAPI"]


class AsyncTreasuryAPI(BaseAsyncAPI):
    async def tax_cap(self, denom: str) -> Coin:
        """Fetches the tax cap for a denom.

        Args:
            denom (str): denom

        Returns:
            Coin: tax cap
        """
        res = await self._c._get(f"/treasury/tax_cap/{denom}")
        return Coin(denom, res)

    async def tax_rate(self) -> Dec:
        """Fetches the current tax rate.

        Returns:
            Dec: tax rate
        """
        res = await self._c._get("/treasury/tax_rate")
        return Dec(res)

    async def reward_weight(self) -> Dec:
        """Fetches the current reward rate.

        Returns:
            Dec: reward weight
        """
        res = await self._c._get("/treasury/reward_weight")
        return Dec(res)

    async def tax_proceeds(self) -> Coins:
        """Fetches the current tax proceeds.

        Returns:
            Coins: tax proceeds
        """
        res = await self._c._get("/treasury/tax_proceeds")
        return Coins.from_data(res)

    async def seigniorage_proceeds(self) -> Coin:
        """Fetches the current seigniorage proceeds.

        Returns:
            Coin: seigniorage proceeds
        """
        res = await self._c._get("/treasury/seigniorage_proceeds")
        return Coin("uluna", res)

    async def parameters(self) -> Coin:
        """Fetches the Treasury module parameters.

        Returns:
            Coin: Treasury module parameters.
        """
        res = await self._c._get("/treasury/parameters")
        return res


class TreasuryAPI(AsyncTreasuryAPI):
    @sync_bind(AsyncTreasuryAPI.tax_cap)
    def tax_cap(self, denom: str) -> Coin:
        pass

    tax_cap.__doc__ = AsyncTreasuryAPI.tax_cap.__doc__

    @sync_bind(AsyncTreasuryAPI.tax_rate)
    def tax_rate(self) -> Dec:
        pass

    tax_rate.__doc__ = AsyncTreasuryAPI.tax_rate.__doc__

    @sync_bind(AsyncTreasuryAPI.reward_weight)
    def reward_weight(self) -> Dec:
        pass

    reward_weight.__doc__ = AsyncTreasuryAPI.reward_weight.__doc__

    @sync_bind(AsyncTreasuryAPI.tax_proceeds)
    def tax_proceeds(self) -> Coins:
        pass

    tax_proceeds.__doc__ = AsyncTreasuryAPI.tax_proceeds.__doc__

    @sync_bind(AsyncTreasuryAPI.seigniorage_proceeds)
    def seigniorage_proceeds(self) -> Coin:
        pass

    seigniorage_proceeds.__doc__ = AsyncTreasuryAPI.seigniorage_proceeds.__doc__

    @sync_bind(AsyncTreasuryAPI.parameters)
    def parameters(self) -> Coin:
        pass

    parameters.__doc__ = AsyncTreasuryAPI.parameters.__doc__
