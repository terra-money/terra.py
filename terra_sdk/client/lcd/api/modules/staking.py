from typing import List, Optional, Union

from terra_sdk.client.lcd.api import ApiResponse, BaseApi, project
from terra_sdk.core import (
    AccAddress,
    Coin,
    Delegation,
    Redelegation,
    UnbondingDelegation,
    ValAddress,
    Validator,
)
from terra_sdk.core.denoms import uLuna
from terra_sdk.util.serdes import terra_sdkBox
from terra_sdk.util.validation import validate_acc_address, validate_val_address

__all__ = ["StakingApi"]


class StakingApi(BaseApi):
    def delegations(
        self,
        delegator: Optional[AccAddress] = None,
        validator: Optional[ValAddress] = None,
    ) -> Union[ApiResponse, List[Delegation]]:
        """Queries the delegation between a delegator and a validator."""
        if delegator is not None and validator is not None:
            delegator = validate_acc_address(delegator)
            validator = validate_val_address(validator)
            res = self._api_get(
                f"/staking/delegators/{delegator}/delegations/{validator}"
            )
            return project(res, [Delegation.deserialize(res)])
        elif delegator:
            delegator = validate_acc_address(delegator)
            res = self._api_get(f"/staking/delegators/{delegator}/delegations")
        elif validator:
            validator = validate_val_address(validator)
            res = self._api_get(f"/staking/validators/{validator}/delegations")
        else:
            raise TypeError("arguments delegator and validator cannot both be None")
        return project(res, [Delegation.deserialize(delgn) for delgn in res])

    def delegation(
        self, delegator: AccAddress, validator: ValAddress
    ) -> Union[ApiResponse, Delegation]:
        return self.delegations(delegator, validator)[0]

    def unbonding_delegations(
        self,
        delegator: Optional[AccAddress] = None,
        validator: Optional[ValAddress] = None,
    ) -> Union[ApiResponse, List[UnbondingDelegation]]:
        if delegator is not None and validator is not None:
            delegator = validate_acc_address(delegator)
            validator = validate_val_address(validator)
            res = self._api_get(
                f"/staking/delegators/{delegator}/unbonding_delegations/{validator}"
            )
            return project(res, [UnbondingDelegation.deserialize(res)])
        elif delegator:
            delegator = validate_acc_address(delegator)
            res = self._api_get(
                f"/staking/delegators/{delegator}/unbonding_delegations"
            )
        elif validator:
            validator = validate_val_address(validator)
            res = self._api_get(
                f"/staking/validators/{validator}/unbonding_delegations"
            )
        else:
            raise TypeError("arguments delegator and validator cannot both be None")
        return project(res, [UnbondingDelegation.deserialize(delgn) for delgn in res])

    def unbonding_delegation(
        self, delegator: AccAddress, validator: ValAddress
    ) -> Union[ApiResponse, UnbondingDelegation]:
        return self.unbonding_delegations(delegator, validator)[0]

    def redelegations(
        self,
        delegator: Optional[AccAddress] = None,
        validator_src: Optional[ValAddress] = None,
        validator_dst: Optional[ValAddress] = None,
    ) -> Union[ApiResponse, List[Redelegation]]:
        params = {}
        if delegator:
            delegator = validate_acc_address(delegator)
            params["delegator"] = delegator
        if validator_src:
            validator_src = validate_val_address(validator_src)
            params["validator_from"] = validator_src
        if validator_dst:
            validator_dst = validate_val_address(validator_dst)
            params["validator_to"] = validator_dst
        res = self._api_get(f"/staking/redelegations", params=params)
        return project(res, [Redelegation.deserialize(rd) for rd in res])

    def bonded_validators_for(
        self, delegator: AccAddress
    ) -> Union[ApiResponse, List[Validator]]:
        delegator = validate_acc_address(delegator)
        vs = self._api_get(f"/staking/delegators/{delegator}/validators")
        return [Validator.deserialize(v) for v in vs]

    def staking_txs_for(self, delegator: AccAddress) -> ApiResponse:
        delegator = validate_acc_address(delegator)
        return self._api_get(f"/staking/delegators/{delegator}/txs", unwrap=False)

    def validators(
        self, status: Optional[str] = None
    ) -> Union[ApiResponse, List[Validator]]:
        params = dict()
        if status is not None:
            params["status"] = status
        res = self._api_get("/staking/validators", params=params)
        return project(res, [Validator.deserialize(v) for v in res])

    def val_info_for(self, validator: ValAddress) -> Union[ApiResponse, Validator]:
        validator = validate_val_address(validator)
        res = self._api_get(f"/staking/validators/{validator}")
        return project(res, Validator.deserialize(res))

    def pool(
        self, key: Optional[str] = None
    ) -> Union[ApiResponse, Coin, terra_sdkBox[str, Coin]]:
        res = self._api_get("/staking/pool")
        pool = terra_sdkBox(
            {
                "bonded": Coin(uLuna, res["bonded_tokens"]),
                "not_bonded": Coin(uLuna, res["not_bonded_tokens"]),
            }
        )
        return project(res, pool[key] if key else pool)

    def params(self, key: Optional[str] = None) -> Union[ApiResponse, terra_sdkBox]:
        res = self._api_get("/staking/parameters")
        p = terra_sdkBox(res, box_recast={"unbonding_time": int})
        return project(res, p[key] if key else p)
