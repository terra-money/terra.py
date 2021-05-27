from terra_sdk.client.lcd import LCDClient

bombay = LCDClient(url="https://bombay-lcd.terra.dev", chain_id="bombay-0001")

parameters = bombay.distribution.parameters()
assert "community_tax" in parameters
assert "base_proposer_reward" in parameters
assert "bonus_proposer_reward" in parameters
assert "withdraw_addr_enabled" in parameters
