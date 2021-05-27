from terra_sdk.client.lcd import LCDClient

bombay = LCDClient(url="https://bombay-lcd.terra.dev", chain_id="bombay-0001")

parameters = bombay.gov.parameters()
assert "deposit_params" in parameters
assert "min_deposit" in parameters["deposit_params"]
assert "max_deposit_period" in parameters["deposit_params"]
assert "voting_params" in parameters
assert "voting_period" in parameters["voting_params"]
assert "tally_params" in parameters
assert "quorum" in parameters["tally_params"]
assert "threshold" in parameters["tally_params"]
assert "veto_threshold" in parameters["tally_params"]
