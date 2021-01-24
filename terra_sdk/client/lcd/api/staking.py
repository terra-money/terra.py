from ._base import BaseAPI

from typing import LIst


class StakingAPI(BaseAPI):
    async def delegations(
        self, delegator: Optional[str] = None, validator: Optional[str] = None
    ) -> List[Delegation]:
        if delegator is not None and validator is not None:
            res = await self._c._get(
                f"/staking/delegators/{delegator}/delegations/{validator}"
            )
            return [Delegation.from_data(res["result"])]
        elif delegator is None:
            res = await self._c._get(f"/staking/delegators/{delegator}/delegations")
            return list(map(Delegation.from_data, res["result"]))
        elif validator is None:
            res = await self._c._get(f"/staking/validators/{validator}/delegations")
            return list(map(Delegation.from_data, res["result"]))
        else:
            raise TypeError("arguments delegator and validator cannot both be None")

    async def delegation(self, delegator: str, validator: str) -> Delegation:
        res = await self._c._get(
            f"/staking/delegators/{delegator}/delegations/{validator}"
        )
        return res["result"]

    async def unbonding_delegations(
        self, delegator: Optional[str] = None, validator: Optional[str] = None
    ) -> List[UnbondingDelegation]:
        if delegator is not None and validator is not None:
            res = await self._c._get(
                f"/staking/delegators/{delegator}/unbonding_delegations/{validator}"
            )
            return [UnbondingDelegation.from_data(res["result"])]
        elif delegator is None:
            res = await self._c._get(
                f"/staking/delegators/{delegator}/unbonding_delegations"
            )
            return list(map(UnbondingDelegation.from_data, res["result"]))
        elif validator is None:
            res = await self._c._get(
                f"/staking/validators/{validator}/unbonding_delegations"
            )
            return list(map(UnbondingDelegation.from_data, res["result"]))
        else:
            raise TypeError("arguments delegator and validator cannot both be None")

    async def unbonding_delegation(
        self, delegator: str, validator: str
    ) -> UnbondingDelegation:
        res = await self._c._get(
            f"/staking/delegators/{delegator}/unbonding_delegations/{validator}"
        )
        return UnbondingDelegation.from_data(res["result"])

    async def redelegations(
        self,
        delegator: Optional[str] = None,
        validator_src: Optional[str] = None,
        validator_dst: Optional[str] = None,
    ) -> List[Redelegation]:
        params = {
            "delegator": delegator,
            "validator_from": validator_src,
            "validator_to": validator_dst
        }
        res = await self._c._get(f"/staking/redelegations", params)
        return list(map(Redelegation.from_data, res["result"]))
    
    async def bonded_validators(self, delegator: str): 
