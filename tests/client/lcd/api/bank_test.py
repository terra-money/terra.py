from terra_sdk.client.lcd import LCDClient
from terra_sdk.client.lcd.params import PaginationOptions

terra = LCDClient(
    url="https://pisco-lcd.terra.dev/",
    chain_id="pisco-1",
)

pagOpt = PaginationOptions(limit=2, count_total=True)


def test_balance():
    result, _ = terra.bank.balance(
        address="terra1rk6tvacasnnyssfnn00zl7wz43pjnpn7vayqv6"
    )
    assert result.to_data()
    assert result.get("uluna").amount > 0


def test_balance_with_pagination():
    result, _ = terra.bank.balance(
        address="terra1rk6tvacasnnyssfnn00zl7wz43pjnpn7vayqv6", params=pagOpt
    )

    assert result.to_data()
    assert result.get("uluna").amount > 0


def test_total():
    result, _ = terra.bank.total()

    assert result.to_data()


def test_total_with_pagination():
    result, _ = terra.bank.total(pagOpt)

    assert result.to_data()


def test_spendable_balances():
    result, _ = terra.bank.spendable_balances(
        address="terra1rk6tvacasnnyssfnn00zl7wz43pjnpn7vayqv6"
    )

    assert result.to_data()
