from terra_sdk.client.lcd import LCDClient
from terra_sdk.client.lcd.api.staking import StakingPool
from terra_sdk.core.staking import (
    Delegation,
    Redelegation,
    UnbondingDelegation,
    Validator,
)

bombay = LCDClient(url="https://bombay-lcd.terra.dev", chain_id="bombay-0001")

parameters = bombay.staking.parameters()
assert "unbonding_time" in parameters
assert "max_validators" in parameters
assert "max_entries" in parameters
assert "historical_entries" in parameters
assert "bond_denom" in parameters
assert "power_reduction" in parameters

validator_address = "terravaloper1qxqrtvg3smlfdfhvwcdzh0huh4f50kfs6gdt4x"
delegator_address = "terra1qxqrtvg3smlfdfhvwcdzh0huh4f50kfs68pk94"

delegations = bombay.staking.delegations(validator=validator_address)
assert type(delegations[0]) == Delegation if len(delegations) > 0 else True

delegations = bombay.staking.delegations(delegator=delegator_address)
assert type(delegations[0]) == Delegation if len(delegations) > 0 else True

delegations = bombay.staking.delegations(delegator_address, validator_address)
assert type(delegations[0]) == Delegation if len(delegations) > 0 else True

delegation = bombay.staking.delegation(delegator_address, validator_address)
assert type(delegation) == Delegation

unbonding_delegations = bombay.staking.unbonding_delegations(
    validator=validator_address
)
assert (
    type(unbonding_delegations[0]) == UnbondingDelegation
    if len(unbonding_delegations) > 0
    else True
)

unbonding_delegations = bombay.staking.unbonding_delegations(
    delegator=delegator_address
)
assert (
    type(unbonding_delegations[0]) == UnbondingDelegation
    if len(unbonding_delegations) > 0
    else True
)

# No results match this query so it throws a 500 series error
# unbonding_delegations = bombay.staking.unbonding_delegations(delegator_address, validator_address)
# assert type(unbonding_delegations[0]) == UnbondingDelegation if len(unbonding_delegations) > 0 else True

# unbonding_delegation = bombay.staking.unbonding_delegation(delegator_address, validator_address)
# assert type(unbonding_delegation) == UnbondingDelegation

validator_dst = "terravaloper1dcegyrekltswvyy0xy69ydgxn9x8x32zdy3ua5"

# No results match this query so it throws a 500 series error
# redelegations = bombay.staking.redelegations(
#     delegator=delegator_address,
#     validator_src=validator_address,
#     validator_dst=validator_dst,
# )
# assert type(redelegations[0]) == Redelegation if len(redelegations) > 0 else True

redelegations = bombay.staking.redelegations(
    delegator=delegator_address,
)
assert type(redelegations[0]) == Redelegation if len(redelegations) > 0 else True

redelegations = bombay.staking.redelegations(
    validator_src=validator_address,
)
assert type(redelegations[0]) == Redelegation if len(redelegations) > 0 else True

redelegations = bombay.staking.redelegations(
    validator_dst=validator_dst,
)
assert type(redelegations[0]) == Redelegation if len(redelegations) > 0 else True

redelegations = bombay.staking.redelegations(
    delegator=delegator_address,
    validator_src=validator_address,
)
assert type(redelegations[0]) == Redelegation if len(redelegations) > 0 else True

redelegations = bombay.staking.redelegations(
    delegator=delegator_address,
    validator_dst=validator_dst,
)
assert type(redelegations[0]) == Redelegation if len(redelegations) > 0 else True

redelegations = bombay.staking.redelegations(
    validator_src=validator_address,
    validator_dst=validator_dst,
)
assert type(redelegations[0]) == Redelegation if len(redelegations) > 0 else True

bonded_validators = bombay.staking.bonded_validators(delegator_address)
assert type(bonded_validators[0]) == Validator if len(bonded_validators) > 0 else True

validators = bombay.staking.validators()
assert type(validators[0]) == Validator if len(validators) > 0 else True

validator = bombay.staking.validator(validator_address)
assert type(validator) == Validator

pool = bombay.staking.pool()
assert type(pool) == StakingPool
