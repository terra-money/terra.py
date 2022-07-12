from terra_sdk.client.lcd import LCDClient, PaginationOptions
from terra_sdk.core import Coins

terra = LCDClient(
    url="https://pisco-lcd.terra.dev/",
    chain_id="pisco-1",
)


def test_query_min_commission():
    # base_account
    result = terra.auth.minimum_commission()

    assert result >= 0
    assert result <= 1

def test_query_ante_params():
    params = terra.ante.parameters()
    
    # assert params.minimum_commission_enforced