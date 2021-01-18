from __future__ import annotations

from typing import Dict, List, Optional, Union

from cached_property import cached_property

from terra_sdk.client.lcd.api import ApiResponse, project
from terra_sdk.client.lcd.api.modules.auth import account_info_type
from terra_sdk.core import (
    AccAddress,
    Coin,
    Coins,
    Delegation,
    Redelegation,
    UnbondingDelegation,
    ValAddress,
    Validator,
)
from terra_sdk.util.validation import validate_val_address


class AccountQuery(object):
    def __init__(self, terra, address: str):
        self.terra = terra
        self.address = AccAddress(address)

    def __str__(self):
        return self.address

    def __repr__(self):
        return f"AccountQuery({self.address!r}) -> {self.terra}"

    @cached_property
    def validator(self):
        return self.terra.validator(self.address.val_address)

    # Auth

    def info(self) -> Union[ApiResponse, account_info_type]:
        return self.terra.auth.acc_info_for(self.address)

    # Bank

    def balance(self, denom: Optional[str] = None) -> Union[ApiResponse, Coin, Coins]:
        res = self.terra.bank.balance_for(self.address)
        return project(res, res[denom] if denom else res)

    # Distribution

    def rewards(
        self, validator: Optional[ValAddress] = None
    ) -> Union[ApiResponse, Dict[ValAddress, Coins], Coins]:
        if validator:
            validator = validate_val_address(validator)
        res = self.terra.distribution.rewards_for(delegator=self.address)
        rewards = res["rewards"]
        return project(res, rewards[validator] if validator else rewards)

    def total_rewards(self, denom: Optional[str] = None) -> Union[ApiResponse, Coins]:
        res = self.terra.distribution.rewards_for(delegator=self.address)
        total = res["total"]
        return project(res, total[denom] if denom else total)

    def withdraw_address(self) -> Union[ApiResponse, AccAddress]:
        return self.terra.distribution.withdraw_address_for(delegator=self.address)

    # Staking

    def delegations(
        self, validator: Optional[ValAddress] = None
    ) -> Union[ApiResponse, List[Delegation]]:
        return self.terra.staking.delegations(
            delegator=self.address, validator=validator
        )

    def unbonding_delegations(
        self, validator: Optional[ValAddress] = None
    ) -> Union[ApiResponse, List[UnbondingDelegation]]:
        return self.terra.staking.unbonding_delegations(
            delegator=self.address, validator=validator
        )

    def redelegations(
        self, validator_src=None, validator_dst=None
    ) -> Union[ApiResponse, List[Redelegation]]:
        return self.terra.staking.redelegations(
            delegator=self.address,
            validator_src=validator_src,
            validator_dst=validator_dst,
        )

    def bonded_validators(self) -> Union[ApiResponse, List[Validator]]:
        return self.terra.staking.bonded_validators_for(delegator=self.address)

    def staking_txs(self):
        return self.terra.staking.staking_txs_for(delegator=self.address)
