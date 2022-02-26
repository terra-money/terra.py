from terra_sdk.client.lcd import LCDClient
from terra_sdk.client.lcd.params import PaginationOptions

terra = LCDClient(
    url="https://bombay-lcd.terra.dev/",
    chain_id="bombay-12",
)
pagOpt = PaginationOptions(limit=2, count_total=True)


def test_balance():
    result, _ = terra.bank.balance(
        address="terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v"
    )
    assert result.to_data()
    assert result.get("ukrw").amount > 0


def test_balance_with_pagination():
    result, _ = terra.bank.balance(
        address="terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v", params=pagOpt
    )
    assert result.to_data()


def test_total():
    result, _ = terra.bank.total()
    assert result.to_data()


def test_total_with_pagination():
    result, _ = terra.bank.total(pagOpt)
    assert result.to_data()
