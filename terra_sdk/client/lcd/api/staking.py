from typing import List, Optional

import attr

from terra_sdk.core import AccAddress, Coin, Numeric, ValAddress
from terra_sdk.core.staking import (
    Delegation,
    Redelegation,
    UnbondingDelegation,
    Validator,
)

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncStakingAPI", "StakingAPI", "StakingPool"]

from ..params import APIParams, PaginationOptions


class RedelegationsOptions(PaginationOptions):
    """just internal class for relegation option"""

    def __init__(
        self,
        src_validator_addr: Optional[str] = None,
        dst_validator_addr: Optional[str] = None,
    ):
        super().__init__(self)
        self.src_validator_addr = src_validator_addr
        self.dst_validator_addr = dst_validator_addr

    def __str__(self):
        return "&".join(self.to_dict())

    def to_dict(self) -> dict:
        params = super().to_dict()
        if self.src_validator_addr is not None:
            params["src_validator_addr"] = self.src_validator_addr
        if self.dst_validator_addr is not None:
            params["dst_validator_addr"] = self.dst_validator_addr
        return params


@attr.s
class StakingPool:
    bonded_tokens: Coin = attr.ib()
    not_bonded_tokens: Coin = attr.ib()


class AsyncStakingAPI(BaseAsyncAPI):
    async def delegations(
        self,
        delegator: Optional[AccAddress] = None,
        validator: Optional[ValAddress] = None,
        params: Optional[APIParams] = None,
    ) -> (List[Delegation], dict):
        """Fetches current delegations, filtering by delegator, validator, or both.

        Args:
            delegator (Optional[AccAddress], optional): delegator account address.
            validator (Optional[ValAddress], optional): validator operator address.
            params (APIParams, optional): additional params for the API like pagination

        Raises:
            TypeError: if both ``delegator`` and ``validator`` are ``None``.

        Returns:
            List[Delegation]: delegations
            dict: pagination info
        """
        if delegator is not None and validator is not None:
            res = await self._c._get(
                f"/cosmos/staking/v1beta1/validators/{validator}/delegations/{delegator}",
                params,
            )
            return [Delegation.from_data(res.get("delegation_response"))], res.get(
                "pagination"
            )
        elif delegator is not None:
            res = await self._c._get(
                f"/cosmos/staking/v1beta1/delegations/{delegator}", params
            )
            return [
                Delegation.from_data(d) for d in res.get("delegation_responses")
            ], res.get("pagination")
        elif validator is not None:
            res = await self._c._get(
                f"/cosmos/staking/v1beta1/validators/{validator}/delegations", params
            )
            return [
                Delegation.from_data(d) for d in res.get("delegation_responses")
            ], res.get("pagination")
        else:
            raise TypeError("arguments delegator and validator cannot both be None")

    async def delegation(
        self, delegator: AccAddress, validator: ValAddress
    ) -> Delegation:
        """Fetch a single delegation via a delegator, validator pair.

        Args:
            delegator (Optional[AccAddress), optional: delegator account address
            validator (Optional[ValAddress], optional): validator operator address

        Returns:
            Delegation: delegation
        """
        res = await self._c._get(
            f"/cosmos/staking/v1beta1/validators/{validator}/delegations/{delegator}"
        )
        res = res.get("delegation_response").get("delegation")
        return res

    async def unbonding_delegations(
        self,
        delegator: Optional[AccAddress] = None,
        validator: Optional[ValAddress] = None,
        params: Optional[APIParams] = None,
    ) -> (List[UnbondingDelegation], dict):
        """Fetches current undelegations, filtering by delegator, validator, or both.

        Args:
            delegator (Optional[AccAddress], optional): delegator account address.
            validator (Optional[ValAddress], optional): validator operator address.
            params (APIParams, optional): additional params for the API like pagination

        Raises:
            TypeError: if both ``delegator`` and ``validator`` are ``None``.

        Returns:
            List[UnbondingDelegation]: undelegations
            dict: pagination info
        """
        if delegator is not None and validator is not None:
            res = await self._c._get(
                f"/cosmos/staking/v1beta1/validators/{validator}/delegations/{delegator}/unbonding_delegation",
                params,
            )
            return [UnbondingDelegation.from_data(res.get("unbond"))], res.get(
                "pagination"
            )
        elif delegator is not None:
            res = await self._c._get(
                f"/cosmos/staking/v1beta1/delegators/{delegator}/unbonding_delegations",
                params,
            )
            return [
                UnbondingDelegation.from_data(x) for x in res.get("unbonding_responses")
            ], res.get("pagination")
        elif validator is not None:
            res = await self._c._get(
                f"/cosmos/staking/v1beta1/validators/{validator}/unbonding_delegations",
                params,
            )
            return [
                UnbondingDelegation.from_data(x) for x in res.get("unbonding_responses")
            ], res.get("pagination")
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
            f"/cosmos/staking/v1beta1/validators/{validator}/delegations/{delegator}/unbonding_delegation"
        )
        return UnbondingDelegation.from_data(res.get("unbond"))

    async def redelegations(
        self,
        delegator: Optional[AccAddress] = None,
        validator_src: Optional[ValAddress] = None,
        validator_dst: Optional[ValAddress] = None,
        params: Optional[APIParams] = None,
    ) -> (List[Redelegation], dict):
        """Fetch redelgations.

        Args:
            delegator (Optional[AccAddress], optional): delegator account address.
            validator_src (Optional[ValAddress], optional): source validator operator address (from).
            validator_dst (Optional[ValAddress], optional): dest. validator operator address (to).
            params (APIParams, optional): additional params for the API like pagination

        Returns:
            List[Redelegation]: redelegations
            dict: pagination info
        """

        # _params = RedelegationsOptions(src_validator_addr=validator_src, dst_validator_addr=validator_dst)
        if params is not None:
            _params = params.to_dict()
        else:
            _params = {}
        _params["src_validator_addr"] = validator_src
        _params["dst_validator_addr"] = validator_dst
        for x in list(_params.keys()):
            if _params[x] is None:
                del _params[x]
        res = await self._c._get(
            f"/cosmos/staking/v1beta1/delegators/{delegator}/redelegations", _params
        )
        return [
            Redelegation.from_data(d) for d in res.get("redelegation_responses")
        ], res.get("pagination")

    async def bonded_validators(
        self, delegator: AccAddress, params: Optional[PaginationOptions]
    ) -> (List[Validator], dict):
        """Fetches the list of validators a delegator is currently delegating to.

        Args:
            delegator (AccAddress): delegator account address
            params (APIParams, optional): additional params for the API like pagination

        Returns:
            List[Validator]: currently bonded validators
            dict: pagination info
        """
        res = await self._c._get(
            f"/cosmos/staking/v1beta1/delegators/{delegator}/validators", params
        )
        return [Validator.from_data(d) for d in res.get("validators")], res.get(
            "pagination"
        )

    async def validators(
        self, params: Optional[APIParams] = None
    ) -> (List[Validator], dict):
        """Fetch information of all validators.

        Args:
            params (APIParams, optional): additional params for the API like pagination

        Returns:
            List[Validator]: validator informations
            dict: pagination info
        """
        res = await self._c._get("/cosmos/staking/v1beta1/validators", params)
        return [Validator.from_data(d) for d in res.get("validators")], res.get(
            "pagination"
        )

    async def validator(self, validator: ValAddress) -> Validator:
        """Fetch information about a single validator.

        Args:
            validator (ValAddress): validator operator address

        Returns:
            Validator: validator information
        """
        res = await self._c._get(f"/cosmos/staking/v1beta1/validators/{validator}")
        return Validator.from_data(res.get("validator"))

    async def pool(self) -> StakingPool:
        """Fetch current staking pool information.

        Returns:
            StakingPool: information about current staking pool
        """
        res = await self._c._get("/cosmos/staking/v1beta1/pool")
        res = res.get("pool")
        return StakingPool(
            bonded_tokens=Coin("uluna", res["bonded_tokens"]),
            not_bonded_tokens=Coin("uluna", res["not_bonded_tokens"]),
        )

    async def parameters(self) -> dict:
        """Fetch Staking module parameters.

        Returns:
            dict: Staking module parameters
        """
        res = await self._c._get("/cosmos/staking/v1beta1/params")
        res = res.get("params")
        return {
            "unbonding_time": res["unbonding_time"],
            "max_validators": Numeric.parse(res["max_validators"]),
            "max_entries": Numeric.parse(res["max_entries"]),
            "historical_entries": Numeric.parse(res["historical_entries"]),
            "bond_denom": res["bond_denom"],
        }


class StakingAPI(AsyncStakingAPI):
    @sync_bind(AsyncStakingAPI.delegations)
    def delegations(
        self,
        delegator: Optional[AccAddress] = None,
        validator: Optional[ValAddress] = None,
        params: Optional[APIParams] = None,
    ) -> (List[Delegation], dict):
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
        params: Optional[APIParams] = None,
    ) -> (List[UnbondingDelegation], dict):
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
        params: Optional[APIParams] = None,
    ) -> (List[Redelegation], dict):
        pass

    redelegations.__doc__ = AsyncStakingAPI.redelegations.__doc__

    @sync_bind(AsyncStakingAPI.bonded_validators)
    def bonded_validators(
        self, delegator: AccAddress, params: Optional[PaginationOptions] = None
    ) -> (List[Validator], dict):
        pass

    bonded_validators.__doc__ = AsyncStakingAPI.bonded_validators.__doc__

    @sync_bind(AsyncStakingAPI.validators)
    def validators(self, params: Optional[APIParams]) -> (List[Validator], dict):
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
