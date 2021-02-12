from typing import List, Optional

import attr

from terra_sdk.core import AccAddress, Coin, ValAddress
from terra_sdk.core.staking import (
    Delegation,
    Redelegation,
    UnbondingDelegation,
    Validator,
)

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncStakingAPI", "StakingAPI", "StakingPool"]


@attr.s
class StakingPool:
    bonded_tokens: Coin = attr.ib()
    not_bonded_tokens: Coin = attr.ib()


class AsyncStakingAPI(BaseAsyncAPI):
    async def delegations(
        self,
        delegator: Optional[AccAddress] = None,
        validator: Optional[ValAddress] = None,
    ) -> List[Delegation]:
        """Fetches current delegations, filtering by delegator, validator, or both.

        Args:
            delegator (Optional[AccAddress], optional): delegator account address.
            validator (Optional[ValAddress], optional): validator operator address.

        Raises:
            TypeError: if both ``delegator`` and ``validator`` are ``None``.

        Returns:
            List[Delegation]: delegations
        """
        if delegator is not None and validator is not None:
            res = await self._c._get(
                f"/staking/delegators/{delegator}/delegations/{validator}"
            )
            return [Delegation.from_data(res)]
        elif delegator is not None:
            res = await self._c._get(f"/staking/delegators/{delegator}/delegations")
            return [Delegation.from_data(d) for d in res]
        elif validator is not None:
            res = await self._c._get(f"/staking/validators/{validator}/delegations")
            return [Delegation.from_data(d) for d in res]
        else:
            raise TypeError("arguments delegator and validator cannot both be None")

    async def delegation(
        self, delegator: AccAddress, validator: ValAddress
    ) -> Delegation:
        """Fetch a single delegation via a delegator, validator pair.

        Args:
            delegator (AccAddress): delegator account address
            validator (ValAddress): validator operator address

        Returns:
            Delegation: delegation
        """
        res = await self._c._get(
            f"/staking/delegators/{delegator}/delegations/{validator}"
        )
        return res

    async def unbonding_delegations(
        self,
        delegator: Optional[AccAddress] = None,
        validator: Optional[ValAddress] = None,
    ) -> List[UnbondingDelegation]:
        """Fetches current undelegations, filtering by delegator, validator, or both.

        Args:
            delegator (Optional[AccAddress], optional): delegator account address.
            validator (Optional[ValAddress], optional): validator operator address.

        Raises:
            TypeError: if both ``delegator`` and ``validator`` are ``None``.

        Returns:
            List[UnbondingDelegation]: undelegations
        """
        if delegator is not None and validator is not None:
            res = await self._c._get(
                f"/staking/delegators/{delegator}/unbonding_delegations/{validator}"
            )
            return [UnbondingDelegation.from_data(res)]
        elif delegator is not None:
            res = await self._c._get(
                f"/staking/delegators/{delegator}/unbonding_delegations"
            )
            return [UnbondingDelegation.from_data(x) for x in res]
        elif validator is not None:
            res = await self._c._get(
                f"/staking/validators/{validator}/unbonding_delegations"
            )
            return [UnbondingDelegation.from_data(x) for x in res]
        else:
            raise TypeError("arguments delegator and validator cannot both be None")

    async def unbonding_delegation(
        self, delegator: AccAddress, validator: ValAddress
    ) -> UnbondingDelegation:
        """Fetch a single undelegation via a delegator, validator pair.

        Args:
            delegator (AccAddress): delegator account address
            validator (ValAddress): validator operator address

        Returns:
            UnbondingDelegation: undelegation
        """
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
        """Fetch redelgations.

        Args:
            delegator (Optional[AccAddress], optional): delegator account address.
            validator_src (Optional[ValAddress], optional): source validator operator address (from).
            validator_dst (Optional[ValAddress], optional): dest. validator operator address (to).

        Returns:
            List[Redelegation]: redelegations
        """
        params = {
            "delegator": delegator,
            "validator_from": validator_src,
            "validator_to": validator_dst,
        }

        for x in list(params.keys()):
            if params[x] is None:
                del params[x]

        res = await self._c._get("/staking/redelegations", params)
        return [Redelegation.from_data(d) for d in res]

    async def bonded_validators(self, delegator: AccAddress) -> List[Validator]:
        """Fetches the list of validators a delegator is currently delegating to.

        Args:
            delegator (AccAddress): delegator account address

        Returns:
            List[Validator]: currently bonded validators
        """
        res = await self._c._get(f"/staking/delegators/{delegator}/validators")
        return [Validator.from_data(d) for d in res]

    async def validators(self) -> List[Validator]:
        """Fetch information of all validators.

        Returns:
            List[Validator]: validator informations
        """
        res = await self._c._get("/staking/validators")
        return [Validator.from_data(d) for d in res]

    async def validator(self, validator: ValAddress) -> Validator:
        """Fetch information about a single validator.

        Args:
            validator (ValAddress): validator operator address

        Returns:
            Validator: validator information
        """
        res = await self._c._get(f"/staking/validators/{validator}")
        return Validator.from_data(res)

    async def pool(self) -> StakingPool:
        """Fetch current staking pool information.

        Returns:
            StakingPool: information about current staking pool
        """
        res = await self._c._get("/staking/pool")
        return StakingPool(
            bonded_tokens=Coin("uluna", res["bonded_tokens"]),
            not_bonded_tokens=Coin("uluna", res["not_bonded_tokens"]),
        )

    async def parameters(self) -> dict:
        """Fetch Staking module parameters.

        Returns:
            dict: Staking module parameters
        """
        res = await self._c._get("/staking/parameters")
        return res


class StakingAPI(AsyncStakingAPI):
    @sync_bind(AsyncStakingAPI.delegations)
    def delegations(
        self,
        delegator: Optional[AccAddress] = None,
        validator: Optional[ValAddress] = None,
    ) -> List[Delegation]:
        pass

    delegations.__doc__ = AsyncStakingAPI.delegations.__doc__

    @sync_bind(AsyncStakingAPI.delegation)
    def delegation(self, delegator: AccAddress, validator: ValAddress) -> Delegation:
        pass

    delegation.__doc__ = AsyncStakingAPI.delegation.__doc__

    @sync_bind(AsyncStakingAPI.unbonding_delegations)
    def unbonding_delegations(
        self,
        delegator: Optional[AccAddress] = None,
        validator: Optional[ValAddress] = None,
    ) -> List[UnbondingDelegation]:
        pass

    unbonding_delegations.__doc__ = AsyncStakingAPI.unbonding_delegations.__doc__

    @sync_bind(AsyncStakingAPI.unbonding_delegation)
    def unbonding_delegation(
        self, delegator: AccAddress, validator: ValAddress
    ) -> UnbondingDelegation:
        pass

    unbonding_delegation.__doc__ = AsyncStakingAPI.unbonding_delegation.__doc__

    @sync_bind(AsyncStakingAPI.redelegations)
    def redelegations(
        self,
        delegator: Optional[AccAddress] = None,
        validator_src: Optional[ValAddress] = None,
        validator_dst: Optional[ValAddress] = None,
    ) -> List[Redelegation]:
        pass

    redelegations.__doc__ = AsyncStakingAPI.redelegations.__doc__

    @sync_bind(AsyncStakingAPI.bonded_validators)
    def bonded_validators(self, delegator: AccAddress) -> List[Validator]:
        pass

    bonded_validators.__doc__ = AsyncStakingAPI.bonded_validators.__doc__

    @sync_bind(AsyncStakingAPI.validators)
    def validators(self) -> List[Validator]:
        pass

    validators.__doc__ = AsyncStakingAPI.validators.__doc__

    @sync_bind(AsyncStakingAPI.validator)
    def validator(self, validator: ValAddress) -> Validator:
        pass

    validator.__doc__ = AsyncStakingAPI.validator.__doc__

    @sync_bind(AsyncStakingAPI.pool)
    def pool(self) -> StakingPool:
        pass

    pool.__doc__ = AsyncStakingAPI.pool.__doc__

    @sync_bind(AsyncStakingAPI.parameters)
    def parameters(self) -> dict:
        pass

    parameters.__doc__ = AsyncStakingAPI.parameters.__doc__
