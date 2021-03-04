from terra_sdk.client.lcd import LCDClient

terra = LCDClient(chain_id="columbus-4", url="https://lcd.terra.dev")
validators_with_voting_power = terra.utils.validators_with_voting_power()
print(validators_with_voting_power)
tax = terra.utils.calculate_tax("100000000uusd")
print(tax)
