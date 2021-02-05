import pytest

from terra_sdk.core import Coin, Coins


def test_clobbers_similar_denom():
    coins1 = Coins([Coin("ukrw", 1000), Coin("uluna", 1000), Coin("uluna", 1000)])

    coinKRW = coins1["ukrw"]
    coinLUNA = coins1["uluna"]

    assert coinKRW.amount == 1000
    assert coinLUNA.amount == 2000


def test_rejects_nonhomogenous_sets():
    with pytest.raises(TypeError) as _:
        Coins(uluna=1000, ukrw=1.234)


def test_from_str():
    int_coins_string = "5ukrw,12uluna"
    dec_coins_string = "2.3ukrw,1.45uluna"
    neg_dec_coins_string = "-1.0ukrw,2.5uluna"

    int_coins = Coins(ukrw=5, uluna="12")
    dec_coins = Coins(
        ukrw=2.3,
        uluna="1.45",
    )

    neg_dec_coins = Coins(
        ukrw="-1.0",
        uluna=2.5,
    )

    assert Coins.from_str(int_coins_string) == int_coins
    assert Coins.from_str(dec_coins_string) == dec_coins
    assert Coins.from_str(neg_dec_coins_string) == neg_dec_coins
