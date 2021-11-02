from typing import Dict

import attr

from terra_sdk.core import AccAddress, Coins, ValAddress

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncDistributionAPI", "DistributionAPI", "Rewards", "ValidatorRewards"]


@attr.s
class Rewards:
    rewards: Dict[ValAddress, Coins] = attr.ib()
    """Delegator rewards, indexed by validator operator address."""

    total: Coins = attr.ib()
    """Total sum of rewards."""


@attr.s
class ValidatorRewards:
    self_bond_rewards: Coins = attr.ib()
    """Rewards for validator accrued from self-delegation."""

    val_commission: Coins = attr.ib()
    """Rewards for validator accrued from delegation commissions."""


class AsyncDistributionAPI(BaseAsyncAPI):
    async def rewards(self, delegator: AccAddress) -> Rewards:
        """Fetches the staking reward data for a delegator.

        Args:
            delegator (AccAddress): delegator account address

        Returns:
            Rewards: delegator rewards
        """
        res = await self._c._get(f"/distribution/delegators/{delegator}/rewards")
        return Rewards(
            rewards={
                item["validator_address"]: Coins.from_data(item["reward"] or [])
                for item in res["rewards"]
            },
            total=Coins.from_data(res["total"]),
        )

    async def validator_rewards(self, validator: ValAddress) -> ValidatorRewards:
        """Fetches the commission reward data for a validator.

        Args:
            validator (ValAddress): validator operator address

        Returns:
            ValidatorRewards: validator rewards
        """
        res = await self._c._get(f"/distribution/validators/{validator}")
        return ValidatorRewards(
            self_bond_rewards=Coins.from_data(res["self_bond_rewards"]),
            val_commission=Coins.from_data(res["val_commission"]["commission"])
        )

    async def withdraw_address(self, delegator: AccAddress) -> AccAddress:
        """Fetches the withdraw address associated with a delegator.

        Args:
            delegator (AccAddress): delegator account address

        Returns:
            AccAddress: withdraw address
        """
        return await self._c._get(
            f"/distribution/delegators/{delegator}/withdraw_address"
        )

    async def community_pool(self) -> Coins:
        """Fetches the community pool.

        Returns:
            Coins: community pool
        """
        res = await self._c._get("/distribution/community_pool")
        return Coins.from_data(res)

    async def parameters(self) -> dict:
        """Fetches the Distribution module parameters.

        Returns:
            dict: Distribution module parameters
        """
        return await self._c._get("/distribution/parameters")


class DistributionAPI(AsyncDistributionAPI):
    @sync_bind(AsyncDistributionAPI.rewards)
    def rewards(self, delegator: AccAddress) -> Rewards:
        pass

    rewards.__doc__ = AsyncDistributionAPI.rewards.__doc__

    @sync_bind(AsyncDistributionAPI.validator_rewards)
    def validator_rewards(self, validator: ValAddress) -> ValidatorRewards:
        pass

    validator_rewards.__doc__ = AsyncDistributionAPI.validator_rewards.__doc__

    @sync_bind(AsyncDistributionAPI.withdraw_address)
    def withdraw_address(self, delegator: AccAddress) -> AccAddress:
        pass

    withdraw_address.__doc__ = AsyncDistributionAPI.withdraw_address.__doc__

    @sync_bind(AsyncDistributionAPI.community_pool)
    def community_pool(self) -> Coins:
        pass

    community_pool.__doc__ = AsyncDistributionAPI.community_pool.__doc__

    @sync_bind(AsyncDistributionAPI.parameters)
    def parameters(self) -> dict:
        pass

    parameters.__doc__ = AsyncDistributionAPI.parameters.__doc__
