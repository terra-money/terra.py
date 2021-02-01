from ._base import BaseAPI

from typing import List, Optional

from terra_sdk.core import Coin, AccAddress, ValAddress
from terra_sdk.core.staking import (
    Delegation,
    UnbondingDelegation,
    Redelegation,
    Validator,
)


class StakingAPI(BaseAPI):
    async def delegations(
        self,
        delegator: Optional[AccAddress] = None,
        validator: Optional[ValAddress] = None,
    ) -> List[Delegation]:
        if delegator is not None and validator is not None:
            res = await self._c._get(
                f"/staking/delegators/{delegator}/delegations/{validator}"
            )
            return [Delegation.from_data(res)]
        elif delegator is None:
            res = await self._c._get(f"/staking/delegators/{delegator}/delegations")
            return list(map(Delegation.from_data, res))
        elif validator is None:
            res = await self._c._get(f"/staking/validators/{validator}/delegations")
            return list(map(Delegation.from_data, res))
        else:
            raise TypeError("arguments delegator and validator cannot both be None")

    async def delegation(
        self, delegator: AccAddress, validator: ValAddress
    ) -> Delegation:
        res = await self._c._get(
            f"/staking/delegators/{delegator}/delegations/{validator}"
        )
        return res

    async def unbonding_delegations(
        self,
        delegator: Optional[AccAddress] = None,
        validator: Optional[ValAddress] = None,
    ) -> List[UnbondingDelegation]:
        if delegator is not None and validator is not None:
            res = await self._c._get(
                f"/staking/delegators/{delegator}/unbonding_delegations/{validator}"
            )
            return [UnbondingDelegation.from_data(res)]
        elif delegator is None:
            res = await self._c._get(
                f"/staking/delegators/{delegator}/unbonding_delegations"
            )
            return [UnbondingDelegation.from_data(x) for x in res]
        elif validator is None:
            res = await self._c._get(
                f"/staking/validators/{validator}/unbonding_delegations"
            )
            return [UnbondingDelegation.from_data(x) for x in res]
        else:
            raise TypeError("arguments delegator and validator cannot both be None")

    async def unbonding_delegation(
        self, delegator: AccAddress, validator: ValAddress
    ) -> UnbondingDelegation:
        res = await self._c._get(
            f"/staking/delegators/{delegator}/unbonding_delegations/{validator}"
        )
        return UnbondingDelegation.from_data(res)

    async def redelegations(
        self,
        delegator: Optional[AccAddress] = None,
        validator_src: Optional[ValAddress] = None,
        validator_dst: Optional[ValAddress] = None,
    ) -> List[Redelegation]:
        params = {
            "delegator": delegator,
            "validator_from": validator_src,
            "validator_to": validator_dst,
        }
        res = await self._c._get(f"/staking/redelegations", params)
        return list(map(Redelegation.from_data, res))

    async def bonded_validators(self, delegator: AccAddress) -> List[Validator]:
        res = await self._c._get(f"/staking/delegators/{delegator}/validators")
        return list(map(Validator.from_data, res))

    async def validators(self) -> List[Validator]:
        res = await self._c._get(f"/staking/validators")
        return list(map(Validator.from_data, res))

    async def validator(self, validator: ValAddress) -> Validator:
        res = await self._c._get(f"/staking/validators/{validator}")
        return Validator.from_data(res)

    async def pool(self) -> dict:
        res = await self._c._get(f"/staking/pool")
        return {
            "bonded_tokens": Coin("uluna", res["bonded_tokens"]),
            "not_bonded_tokens": Coin("uluna", res["not_bonded_tokens"]),
        }

    async def parameters(self) -> dict:
        res = await self._c._get(f"/staking/parameters")
        return res["parameters"]
