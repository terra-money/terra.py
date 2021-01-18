import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st
from hypothesis_jsonschema import from_schema

from terra_sdk.core import Coin, Coins
from testtools import assert_serdes_consistent, assert_serdes_exact


@pytest.mark.sdk
class TestCoinsSerdes:
    @pytest.mark.serdes
    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(c=from_schema(Coins.__schema__))
    def test_serdes_consistent(self, c):
        assert_serdes_consistent(Coins, c)


@pytest.mark.sdk
class TestCoins:
    def test_constructor_copy(self):
        """sdk.Coins object should copy another sdk.Coins object when passed into constructor,
        rather than maintaining original references."""
        A = Coin("A", 1000)
        C1 = Coins([A])
        C2 = Coins(C1)

        assert C1 == C2
        assert list(C1) == list(C2)
        assert C1 is not C2
        assert C1.coins[0] is not A  # should be a new coin
        assert C2.coins[0] is not C1.coins[0]  # should be a new coin

    def test_converts_to_sorted_list(self):
        """sdk.Coins object should convert to sorted List[Coin] by alphabetic denom."""
        A = Coins([Coin("Z", 500), Coin("A", 1000)])
        B = [Coin("A", 1000), Coin("Z", 500)]
        assert list(A) == B

    def test_equality(self):
        """sdk.Coins object should be able to compare with coins and list."""
        A = Coins([Coin("A", 1000), Coin("B", 500)])
        B = Coins([Coin("B", 500), Coin("A", 1000)])
        assert A == B  # order of original input should not matter
        assert A == [Coin("A", 1000), Coin("B", 500)]
        assert [Coin("A", 1000), Coin("B", 500)] == A
        assert A == [Coin("B", 500), Coin("A", 1000)]
        assert [Coin("B", 500), Coin("A", 1000)] == A
        assert not (A == [500, 1000])
        assert not ([500, 1000] == A)

    def test_getitem(self):
        """sdk.Coins object should act like a dict, and indexable by denom as key."""

        X = Coins([Coin("A", 1000), Coin("B", 2000), Coin("C", 3000)])
        assert all(isinstance(X[i], Coin) for i in ["A", "B", "C"])
        assert X["A"] == Coin("A", 1000)
        assert X["B"] == Coin("B", 2000)
        assert X["C"] == Coin("C", 3000)
        with pytest.raises(KeyError):
            X["D"]

    def test_contains_denom(self):
        """The `in` operator in Python should allow a user to query whether a Coin of a specified denom
        exists in the sdk.Coins object."""

        haystack = Coins(
            [Coin("A", 1000), Coin("B", 500), Coin("needle", 250), Coin("C", 125)]
        )
        assert "needle" in haystack
        assert "B" in haystack
        assert "D" not in haystack

    @pytest.mark.parametrize("t", [list, Coins])
    def test_add_coins(self, t):
        """Coins can be added, which merges the collections of Coins and groups together
        the sum amount for Coins of a similar denom."""
        A = t([Coin("uluna", 2000)])
        B = t([Coin("ukrw", 1000)])
        C = t([Coin("uluna", 1000), Coin("ukrw", 250), Coin("uusd", 2000)])
        assert A + B == Coins([Coin("uluna", 2000), Coin("ukrw", 1000)])
        assert A + B + C == Coins(
            [Coin("uluna", 3000), Coin("ukrw", 1250), Coin("uusd", 2000)]
        )
