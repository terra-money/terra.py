from typing import Dict, Optional, Union

from terra_sdk.client.lcd.api import ApiResponse, BaseApi, project
from terra_sdk.core import AccAddress, Coin, Coins, Dec, ValAddress
from terra_sdk.util.serdes import terra_sdkBox
from terra_sdk.util.validation import validate_acc_address, validate_val_address

__all__ = ["DistributionApi"]


class DistributionApi(BaseApi):
    def rewards_for(self, delegator: AccAddress) -> Union[ApiResponse, dict]:
        """Get an account's delegation rewards."""
        delegator = validate_acc_address(delegator)
        res = self._api_get(f"/distribution/delegators/{delegator}/rewards")
        rewards = res["rewards"] or []
        total = Coins.from_data(res["total"])
        result = terra_sdkBox(
            {
                "rewards": {
                    r["validator_address"]: Coins.deserialize(r["reward"])
                    for r in rewards
                },
                "total": total,
            }
        )
        return project(res, result)

    # def reward(self, delegator: AccAddress, validator: ValAddress):
    #     """Get the delegation reward between a delegator and validator."""
    #     delegator = validate_acc_address(delegator)
    #     validator = validate_val_address(validator)
    #     res =  self.rewards_for(delegator)
    #     return project(res, res["via"]["validator"])

    def withdraw_address_for(
        self, delegator: AccAddress
    ) -> Union[ApiResponse, AccAddress]:
        delegator = validate_acc_address(delegator)
        return self._api_get(f"/distribution/delegators/{delegator}/withdraw_address")

    def val_rewards_for(
        self, validator: ValAddress, key: Optional[str] = None
    ) -> Union[ApiResponse, Coins, Dict[str, Coins]]:
        validator = validate_val_address(validator)
        res = self._api_get(f"/distribution/validators/{validator}")
        rewards = terra_sdkBox(
            {
                "self_bond": Coins.deserialize(res["self_bond_rewards"]),
                "commission": Coins.deserialize(res["val_commission"]),
            }
        )
        return project(res, rewards[key] if key else rewards)

    def community_pool(
        self, denom: Optional[str] = None
    ) -> Union[ApiResponse, Coin, Coins]:
        res = self._api_get("/distribution/community_pool")
        cp = Coins.deserialize(res)
        return project(res, cp[denom] if denom else cp)

    def params(self, key: Optional[str] = None) -> Union[ApiResponse, dict, Dec, bool]:
        res = self._api_get("/distribution/parameters")
        p = res
        p["community_tax"] = Dec(p["community_tax"])
        p["base_proposer_reward"] = Dec(p["base_proposer_reward"])
        p["bonus_proposer_reward"] = Dec(p["bonus_proposer_reward"])
        return project(res, p[key] if key else terra_sdkBox(p))
