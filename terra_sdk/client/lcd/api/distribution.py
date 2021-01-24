from ._base import BaseAPI


class DistributionAPI(BaseAPI):
    async def rewards(self, delegator: str):
        return await self._c._get(f"/distribution/delegators/{delegator}/rewards")

    async def validator_rewards(self, validator: str):
        return await self._c._get(f"/distribution/validators/${validator}")

    async def withdraw_address(self, delegator: str):
        return await self._c._get(
            f"/distribution/delegators/{delegator}/withdraw_address"
        )

    async def community_pool(self):
        return await self._c._get(f"/distribution/community_pool")

    async def parameters(self):
        return await self._c._get(f"/distribution/parameters")
