from terra_sdk.client.lcd import LCDClient, PaginationOptions

terra = LCDClient(
    url="https://bombay-lcd.terra.dev/",
    chain_id="bombay-12",
)


def test_account_info():
    result = terra.auth.account_info("terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v")

    assert(result.address == "terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v")
    assert(result.account_number == 1165)