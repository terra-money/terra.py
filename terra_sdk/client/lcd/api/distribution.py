from typing import Dict, Optional

import attr

from terra_sdk.core import AccAddress, Coins, ValAddress
from ..params import APIParams
from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncDistributionAPI", "DistributionAPI", "Rewards"]


@attr.s
class Rewards:
    rewards: Dict[ValAddress, Coins] = attr.ib()
    """Delegator rewards, indexed by validator operator address."""

    total: Coins = attr.ib()
    """Total sum of rewards."""


class AsyncDistributionAPI(BaseAsyncAPI):
    async def rewards(self, delegator: AccAddress,  params: Optional[APIParams] = None) -> Rewards:
        """Fetches the staking reward data for a delegator.

        Args:
            delegator (AccAddress): delegator account address
            params (APIParams): optional parameters

        Returns:
            Rewards: delegator rewards
        """
        res = await self._c._get(
            f"/cosmos/distribution/v1beta1/delegators/{delegator}/rewards",
            params
        )
        return Rewards(
            rewards={
                item["validator_address"]: Coins.from_data(item["reward"] or [])
                for item in res["rewards"]
            },
            total=Coins.from_data(res["total"]),
        )

    async def validator_commission(self, validator: ValAddress,  params: Optional[APIParams] = None) -> Coins:
        """Fetches the commission reward data for a validator.

        Args:
            validator (ValAddress): validator operator address
            params (APIParams): optional parameters

        Returns:
            ValidatorCommission: validator rewards
        """
        res = await self._c._get(
            f"/cosmos/distribution/v1beta1/validators/{validator}/commission",
            params
        )
        commission = res["commission"]
        return Coins.from_data(commission["commission"])

    async def withdraw_address(self, delegator: AccAddress,  params: Optional[APIParams] = None) -> AccAddress:
        """Fetches the withdraw address associated with a delegator.

        Args:
            delegator (AccAddress): delegator account address
            params (APIParams): optional parameters

        Returns:
            AccAddress: withdraw address
        """
        res = await self._c._get(
            f"/cosmos/distribution/v1beta1/delegators/{delegator}/withdraw_address",
            params
        )
        return res.get("withdraw_address")

    async def community_pool(self,  params: Optional[APIParams] = None) -> Coins:
        """Fetches the community pool.
        Args:
            params (APIParams): optional parameters

        Returns:
            Coins: community pool
        """
        res = await self._c._get("/cosmos/distribution/v1beta1/community_pool",params)
        return Coins.from_data(res.get("pool"))

    async def parameters(self, params: Optional[APIParams] = None) -> dict:
        """Fetches the Distribution module parameters.
        Args:
            params (APIParams): optional parameters

        Returns:
            dict: Distribution module parameters
        """
        res = await self._c._get("/cosmos/distribution/v1beta1/params", params)
        return res.get("params")


class DistributionAPI(AsyncDistributionAPI):
    @sync_bind(AsyncDistributionAPI.rewards)
    def rewards(self, delegator: AccAddress, params: Optional[APIParams] = None) -> Rewards:
        pass

    rewards.__doc__ = AsyncDistributionAPI.rewards.__doc__

    @sync_bind(AsyncDistributionAPI.validator_commission)
    def validator_commission(self, validator: ValAddress, params: Optional[APIParams] = None) -> Coins:
        pass

    validator_commission.__doc__ = AsyncDistributionAPI.validator_commission.__doc__

    @sync_bind(AsyncDistributionAPI.withdraw_address)
    def withdraw_address(self, delegator: AccAddress, params: Optional[APIParams] = None) -> AccAddress:
        pass

    withdraw_address.__doc__ = AsyncDistributionAPI.withdraw_address.__doc__

    @sync_bind(AsyncDistributionAPI.community_pool)
    def community_pool(self, params: Optional[APIParams] = None) -> Coins:
        pass

    community_pool.__doc__ = AsyncDistributionAPI.community_pool.__doc__

    @sync_bind(AsyncDistributionAPI.parameters)
    def parameters(self, params: Optional[APIParams] = None) -> dict:
        pass

    parameters.__doc__ = AsyncDistributionAPI.parameters.__doc__
