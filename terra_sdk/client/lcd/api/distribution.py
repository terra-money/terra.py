from terra_sdk.core import AccAddress, Coins, ValAddress

from ._base import BaseAPI


class DistributionAPI(BaseAPI):
    async def rewards(self, delegator: AccAddress) -> dict:
        res = await self._c._get(f"/distribution/delegators/{delegator}/rewards")
        return {
            "rewards": {
                item["validator_address"]: Coins.from_data(item["reward"] or [])
                for item in res["rewards"]
            },
            "total": Coins.from_data(res["total"]),
        }

    async def validator_rewards(self, validator: ValAddress) -> dict:
        res = await self._c._get(f"/distribution/validators/{validator}")
        return {
            "self_bond_rewards": Coins.from_data(res["self_bond_rewards"]),
            "val_commission": Coins.from_data(res["val_commission"]),
        }

    async def withdraw_address(self, delegator: AccAddress) -> AccAddress:
        return await self._c._get(
            f"/distribution/delegators/{delegator}/withdraw_address"
        )

    async def community_pool(self) -> Coins:
        res = await self._c._get("/distribution/community_pool")
        return Coins.from_data(res)

    async def parameters(self) -> dict:
        return await self._c._get("/distribution/parameters")
