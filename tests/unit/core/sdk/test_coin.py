import pytest
from hypothesis import assume, given
from hypothesis import strategies as st
from hypothesis_jsonschema import from_schema

from terra_sdk.core import Coin, Dec
from terra_sdk.core.denoms import uKRW, uLuna
from terra_sdk.error import DenomIncompatibleError
from testtools import assert_serdes_consistent, assert_serdes_exact


@pytest.fixture
def d1(scope="session"):
    return uLuna


@pytest.fixture
def d2(scope="session"):
    return uKRW


coin_amount = st.one_of(st.integers(), from_schema(Dec.__schema__).map(Dec))


@pytest.mark.sdk
class TestCoinSerdes:
    @pytest.mark.serdes
    @given(c=from_schema(Coin.__schema__))
    def test_serdes_consistent(self, c):
        assert_serdes_consistent(Coin, c)

    def test_uses_correct_internal_amount(self, d1):
        examples = [
            (500, int),
            ("4.2", Dec),
            ("0", int),
            ("0.0", Dec),
            (-100000000000, int),
            ("-0.00000000000001", Dec),
        ]
        for x in examples:
            coin = Coin(d1, x[0])
            assert isinstance(coin.amount, x[1])


@pytest.mark.sdk
class TestCoinOperations:
    def test_make_coin(self, d1):
        coin = Coin(d1, "13929")
        assert coin.denom == d1
        assert coin.amount == 13929

        coin = Coin(d1, "0.006250000000000000")
        assert coin.denom == d1
        assert coin.amount == Dec("0.00625")

    @given(x=st.integers())
    def test_coin_amount_type(self, x, d1):
        # should not be different with integers
        coin = Coin(d1, x)
        coin2 = Coin(d1, str(x))
        assert coin.amount == coin2.amount

    @given(x=coin_amount, y=coin_amount)
    def test_coin_eq(self, x, y, d1, d2):
        """Tests Coin equality against another Coin."""
        assume(x != y)

        coin = Coin(d1, x)
        coin2 = Coin(d1, x)
        assert coin == coin2

        # denoms different
        coin3 = Coin(d1, x)
        coin4 = Coin(d2, x)
        assert coin3 != coin4

        # amount different
        coin5 = Coin(d1, x)
        coin6 = Coin(d1, y)
        assert coin5 != coin6

        # amount type different
        coin7 = Coin(d1, 4)
        coin8 = Coin(d1, "4.2")
        coin9 = Coin(d1, 4.2)
        assert coin7 != coin8
        assert coin8 == coin9

    @given(x=coin_amount, y=coin_amount)
    def test_coin_add(self, d1, d2, x, y):
        coin = Coin(d1, x)
        coin2 = Coin(d1, y)
        coin3 = Coin(d1, x + y)
        coinsum = coin + coin2

        assert isinstance(coinsum.amount, int) or isinstance(coinsum.amount, Dec)
        assert coin3 == coinsum
        with pytest.raises(DenomIncompatibleError):
            Coin(d1, x) + Coin(d2, x)

    @given(x=coin_amount, y=coin_amount)
    def test_coin_sub(self, d1, d2, x, y):
        coin = Coin(d1, x)
        coin2 = Coin(d1, y)
        coin3 = Coin(d1, x - y)
        coindiff = coin - coin2

        assert isinstance(coindiff.amount, int) or isinstance(coindiff.amount, Dec)
        assert coin3 == coindiff
        with pytest.raises(DenomIncompatibleError):
            Coin(d1, x) - Coin(d2, x)

    @given(x=coin_amount, y=coin_amount)
    def test_coin_compare(self, d1, d2, x, y):
        assume(x < y)
        coin = Coin(d1, x)
        coin2 = Coin(d1, y)
        coin3 = Coin(d2, x)

        coin_dup = Coin(d1, x)
        assert coin < coin2
        assert coin2 > coin

        assert coin >= coin_dup
        assert coin <= coin_dup

        with pytest.raises(DenomIncompatibleError):
            coin < coin3

    # TODO: write tests for mul, div, floordiv
