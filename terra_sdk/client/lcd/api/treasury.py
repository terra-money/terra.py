from typing import Optional

from terra_sdk.core import Coin, Coins, Dec, Numeric
from terra_sdk.core.treasury import PolicyConstraints

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
        res = await self._c._get(f"/terra/treasury/v1beta1/tax_caps/{denom}")
        return Coin(denom, res.get("tax_cap"))

    async def tax_rate(self, height: Optional[int] = None) -> Dec:
        """Fetches the current tax rate.

        Returns:
            Dec: tax rate
        """
        params = None
        if height is not None:
            params = {"height": height}
        res = await self._c._get("/terra/treasury/v1beta1/tax_rate", params)
        return Dec(res.get("tax_rate"))

    async def reward_weight(self) -> Dec:
        """Fetches the current reward rate.

        Returns:
            Dec: reward weight
        """
        res = await self._c._get("//terra/treasury/v1beta1/reward_weight")
        return Dec(res.get("reward_weight"))

    async def tax_proceeds(self) -> Coins:
        """Fetches the current tax proceeds.

        Returns:
            Coins: tax proceeds
        """
        res = await self._c._get("/terra/treasury/v1beta1/tax_proceeds")
        return Coins.from_data(res.get("tax_proceeds"))

    async def seigniorage_proceeds(self) -> Coin:
        """Fetches the current seigniorage proceeds.

        Returns:
            Coin: seigniorage proceeds
        """
        res = await self._c._get("/terra/treasury/v1beta1/seigniorage_proceeds")
        return Coin("uluna", res.get("seigniorage_proceeds"))

    async def parameters(self) -> Coin:
        """Fetches the Treasury module parameters.

        Returns:
            Coin: Treasury module parameters.
        """
        res = await self._c._get("/terra/treasury/v1beta1/params")
        params = res.get("params")
        return {
            "tax_policy": PolicyConstraints.from_data(params["tax_policy"]),
            "reward_policy": PolicyConstraints.from_data(params["reward_policy"]),
            "mining_increment": Dec(params["mining_increment"]),
            "seigniorage_burden_target": Dec(params["seigniorage_burden_target"]),
            "window_long": Numeric.parse(params["window_long"]),
            "window_short": Numeric.parse(params["window_short"]),
            "window_probation": Numeric.parse(params["window_probation"]),
        }


class TreasuryAPI(AsyncTreasuryAPI):
    @sync_bind(AsyncTreasuryAPI.tax_cap)
    def tax_cap(self, denom: str) -> Coin:
        pass

    tax_cap.__doc__ = AsyncTreasuryAPI.tax_cap.__doc__

    @sync_bind(AsyncTreasuryAPI.tax_rate)
    def tax_rate(self, height: Optional[int] = None) -> Dec:
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
