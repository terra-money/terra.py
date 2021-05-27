from terra_sdk.client.lcd import LCDClient
from terra_sdk.client.lcd.api.distribution import Rewards, ValidatorRewards
from terra_sdk.core import AccAddress, Coins

bombay = LCDClient(url="https://bombay-lcd.terra.dev", chain_id="bombay-0001")

parameters = bombay.distribution.parameters()
assert "community_tax" in parameters
assert "base_proposer_reward" in parameters
assert "bonus_proposer_reward" in parameters
assert "withdraw_addr_enabled" in parameters

community_pool = bombay.distribution.community_pool()
assert type(community_pool) == Coins

validator_address = "terravaloper1qxqrtvg3smlfdfhvwcdzh0huh4f50kfs6gdt4x"

validator_rewards = bombay.distribution.validator_rewards(validator_address)
assert type(validator_rewards) == ValidatorRewards

delegator_address = "terra1qxqrtvg3smlfdfhvwcdzh0huh4f50kfs68pk94"

rewards = bombay.distribution.rewards(delegator_address)
assert type(rewards) == Rewards

withdraw_addr = bombay.distribution.withdraw_address(delegator_address)
assert type(withdraw_addr) in (AccAddress, AccAddress.__supertype__)
