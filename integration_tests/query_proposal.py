from terra_sdk.client.lcd import LCDClient

terra = LCDClient(chain_id="pisco-1", url="https://pisco-lcd.terra.dev")
res = terra.gov.deposits(proposal_id=5333)
print(res)
res = terra.gov.votes(proposal_id=5333)
print(res)
