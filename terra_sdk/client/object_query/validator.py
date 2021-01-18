from __future__ import annotations

from typing import List, Optional, Union

from cached_property import cached_property

import terra_sdk.client.object_query
import terra_sdk.client.terra
from terra_sdk.client.lcd.api import ApiResponse
from terra_sdk.core import (
    AccAddress,
    Delegation,
    ExchangeRatePrevote,
    ExchangeRateVote,
    Redelegation,
    UnbondingDelegation,
    ValAddress,
    Validator
)


class ValidatorQuery(object):
    def __init__(self, terra: terra_sdk.client.terra.Terra, val_address: ValAddress):
        self.terra = terra
        self.val_address = ValAddress(val_address)

    def __str__(self):
        return self.val_address

    def __repr__(self):
        return f"ValidatorQuery({self.val_address!r}) -> {self.terra}"

    # Staking
    def info(self) -> Validator:
        return self.terra.staking.val_info_for(self.val_address)

    @cached_property
    def account(self):
        return self.terra.account(self.val_address.acc_address)

    def delegations(
        self, delegator: Optional[AccAddress] = None
    ) -> Union[ApiResponse, List[Delegation]]:
        return self.terra.staking.delegations(
            validator=self.val_address, delegator=delegator
        )

    def unbonding_delegations(
        self, delegator: Optional[AccAddress] = None
    ) -> Union[ApiResponse, List[UnbondingDelegation]]:
        return self.terra.staking.unbonding_delegations(
            validator=self.val_address, delegator=delegator
        )

    def outbound_redelegations(
        self, delegator: AccAddress = None, validator_to: ValAddress = None
    ) -> Union[ApiResponse, List[Redelegation]]:
        return self.terra.staking.redelegations()

    def incoming_redelegations(
        self, delegator: AccAddress = None, validator_from: ValAddress = None
    ) -> Union[ApiResponse, List[Redelegation]]:
        return self.terra.staking.redelegations()

    def val_rewards(self, key: Optional[str] = None):
        return self.terra.distribution.val_rewards_for(self.val_address, key)

    # Oracle
    def feeder(self) -> terra_sdk.client.object_query.AccountQuery:
        return self.terra.account(
            self.terra.oracle.feeder_address_for(validator=self.val_address)
        )

    def misses(self) -> int:
        return self.terra.oracle.misses_for(validator=self.val_address)

    def votes(
        self, denom: Optional[str] = None
    ) -> Union[ApiResponse, List[ExchangeRateVote]]:
        return self.terra.oracle.votes(validator=self.val_address, denom=denom)

    def prevotes(
        self, denom: Optional[str] = None
    ) -> Union[ApiResponse, List[ExchangeRatePrevote]]:
        return self.terra.oracle.prevotes(validator=self.val_address, denom=denom)
