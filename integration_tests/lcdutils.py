from terra_sdk.client.lcd import LCDClient

terra = LCDClient(chain_id="bombay-0001", url="http://3.34.120.243:1317")
validators_with_voting_power = terra.utils.validators_with_voting_power()
print(validators_with_voting_power)
tax = terra.utils.calculate_tax("100000000uusd")
print(tax)
