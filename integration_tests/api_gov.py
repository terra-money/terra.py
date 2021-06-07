from terra_sdk.client.lcd import LCDClient
from terra_sdk.core.gov import Proposal

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

proposal_id = "14"

proposal = bombay.gov.proposal(proposal_id)
assert type(proposal) == Proposal

# TODO: Add proposal data to genesis and then add rest of coverage cases

# proposer = bombay.gov.proposer(proposal_id)
# assert type(proposer) == str

# desposits = bombay.gov.deposits(proposal_id)
# assert desposits is not None
