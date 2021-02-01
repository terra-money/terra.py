from ._base import BaseAPI

from terra_sdk.core import AccAddress, ValAddress


class DistributionAPI(BaseAPI):
    async def rewards(self, delegator: AccAddress) -> dict:
        return await self._c._get(f"/distribution/delegators/{delegator}/rewards")

    async def validator_rewards(self, validator: ValAddress) -> dict:
        return await self._c._get(f"/distribution/validators/${validator}")

    async def withdraw_address(self, delegator: AccAddress) -> AccAddress:
        return await self._c._get(
            f"/distribution/delegators/{delegator}/withdraw_address"
        )

    async def community_pool(self):
        return await self._c._get(f"/distribution/community_pool")

    async def parameters(self) -> dict:
        return await self._c._get(f"/distribution/parameters")
