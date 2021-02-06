from typing import List, Optional

import attr

from terra_sdk.core import AccAddress, Coin, ValAddress
from terra_sdk.core.staking import (
    Delegation,
    Redelegation,
    UnbondingDelegation,
    Validator,
)

from ._base import BaseAPI


@attr.s
class StakingPool:
    bonded_tokens: Coin = attr.ib()
    not_bonded_tokens: Coin = attr.ib()


class AsyncStakingAPI(BaseAPI):
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

        for x in list(params.keys()):
            if params[x] is None:
                del params[x]

        res = await self._c._get("/staking/redelegations", params)
        return [Redelegation.from_data(d) for d in res]

    async def bonded_validators(self, delegator: AccAddress) -> List[Validator]:
        res = await self._c._get(f"/staking/delegators/{delegator}/validators")
        return [Validator.from_data(d) for d in res]

    async def validators(self) -> List[Validator]:
        res = await self._c._get("/staking/validators")
        return [Validator.from_data(d) for d in res]

    async def validator(self, validator: ValAddress) -> Validator:
        res = await self._c._get(f"/staking/validators/{validator}")
        return Validator.from_data(res)

    async def pool(self) -> StakingPool:
        res = await self._c._get("/staking/pool")
        return StakingPool(
            bonded_tokens=Coin("uluna", res["bonded_tokens"]),
            not_bonded_tokens=Coin("uluna", res["not_bonded_tokens"]),
        )

    async def parameters(self) -> dict:
        res = await self._c._get("/staking/parameters")
        return res


class StakingAPI(BaseAPI):
    def delegations(
        self,
        delegator: Optional[AccAddress] = None,
        validator: Optional[ValAddress] = None,
    ) -> List[Delegation]:
        """Fetches current delegations, filtering by delegator, validator, or both.

        Args:
            delegator (Optional[AccAddress], optional): delegator account address. Defaults to None.
            validator (Optional[ValAddress], optional): validator operator address. Defaults to None.

        Raises:
            TypeError: if both ``delegator`` and ``validator`` are ``None``.

        Returns:
            List[Delegation]: delegations
        """
        if delegator is not None and validator is not None:
            res = self._c._get(
                f"/staking/delegators/{delegator}/delegations/{validator}"
            )
            return [Delegation.from_data(res)]
        elif delegator is not None:
            res = self._c._get(f"/staking/delegators/{delegator}/delegations")
            return [Delegation.from_data(d) for d in res]
        elif validator is not None:
            res = self._c._get(f"/staking/validators/{validator}/delegations")
            return [Delegation.from_data(d) for d in res]
        else:
            raise TypeError("arguments delegator and validator cannot both be None")

    def delegation(self, delegator: AccAddress, validator: ValAddress) -> Delegation:
        """Fetch a single delegation via a delegator, validator pair.

        Args:
            delegator (AccAddress): delegator account address
            validator (ValAddress): validator operator address

        Returns:
            Delegation: delegation
        """
        res = self._c._get(f"/staking/delegators/{delegator}/delegations/{validator}")
        return res

    def unbonding_delegations(
        self,
        delegator: Optional[AccAddress] = None,
        validator: Optional[ValAddress] = None,
    ) -> List[UnbondingDelegation]:
        """Fetches current undelegations, filtering by delegator, validator, or both.

        Args:
            delegator (Optional[AccAddress], optional): delegator account address. Defaults to None.
            validator (Optional[ValAddress], optional): validator operator address. Defaults to None.

        Raises:
            TypeError: if both ``delegator`` and ``validator`` are ``None``.

        Returns:
            List[UnbondingDelegation]: undelegations
        """
        if delegator is not None and validator is not None:
            res = self._c._get(
                f"/staking/delegators/{delegator}/unbonding_delegations/{validator}"
            )
            return [UnbondingDelegation.from_data(res)]
        elif delegator is not None:
            res = self._c._get(f"/staking/delegators/{delegator}/unbonding_delegations")
            return [UnbondingDelegation.from_data(x) for x in res]
        elif validator is not None:
            res = self._c._get(f"/staking/validators/{validator}/unbonding_delegations")
            return [UnbondingDelegation.from_data(x) for x in res]
        else:
            raise TypeError("arguments delegator and validator cannot both be None")

    def unbonding_delegation(
        self, delegator: AccAddress, validator: ValAddress
    ) -> UnbondingDelegation:
        """Fetch a single undelegation via a delegator, validator pair.

        Args:
            delegator (AccAddress): delegator account address
            validator (ValAddress): validator operator address

        Returns:
            UnbondingDelegation: undelegation
        """
        res = self._c._get(
            f"/staking/delegators/{delegator}/unbonding_delegations/{validator}"
        )
        return UnbondingDelegation.from_data(res)

    def redelegations(
        self,
        delegator: Optional[AccAddress] = None,
        validator_src: Optional[ValAddress] = None,
        validator_dst: Optional[ValAddress] = None,
    ) -> List[Redelegation]:
        """Fetch redelgations.

        Args:
            delegator (Optional[AccAddress], optional): delegator account address. Defaults to None.
            validator_src (Optional[ValAddress], optional): source validator operator address (from). Defaults to None.
            validator_dst (Optional[ValAddress], optional): dest. validator operator address (to). Defaults to None.

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

        res = self._c._get("/staking/redelegations", params)
        return [Redelegation.from_data(d) for d in res]

    def bonded_validators(self, delegator: AccAddress) -> List[Validator]:
        """Fetches the list of validators a delegator is currently delegating to.

        Args:
            delegator (AccAddress): delegator account address

        Returns:
            List[Validator]: currently bonded validators
        """
        res = self._c._get(f"/staking/delegators/{delegator}/validators")
        return [Validator.from_data(d) for d in res]

    def validators(self) -> List[Validator]:
        """Fetch information of all validators.

        Returns:
            List[Validator]: validator informations
        """
        res = self._c._get("/staking/validators")
        return [Validator.from_data(d) for d in res]

    def validator(self, validator: ValAddress) -> Validator:
        """Fetch information about a single validator.

        Args:
            validator (ValAddress): validator operator address

        Returns:
            Validator: validator information
        """
        res = self._c._get(f"/staking/validators/{validator}")
        return Validator.from_data(res)

    def pool(self) -> StakingPool:
        """Fetch current staking pool information.

        Returns:
            StakingPool: information about current staking pool
        """
        res = self._c._get("/staking/pool")
        return StakingPool(
            bonded_tokens=Coin("uluna", res["bonded_tokens"]),
            not_bonded_tokens=Coin("uluna", res["not_bonded_tokens"]),
        )

    def parameters(self) -> dict:
        """Fetch Staking module parameters.

        Returns:
            dict: Staking module parameters
        """
        res = self._c._get("/staking/parameters")
        return res
