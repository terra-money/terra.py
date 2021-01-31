from terra_sdk.core import Coin


def test_eq():
    coin1 = Coin("uluna", 1000)
    coin2 = Coin("uluna", 1000)
    coin3 = Coin("uluna", 1001)

    assert coin1 == coin2
    assert coin1 != coin3


def test_to_str():
    coin1 = Coin("uluna", 123456)
    coin2 = Coin("uluna", 123456.789)

    assert str(coin1) == "123456uluna"
    assert str(coin1.to_dec_coin()) == "123456.0uluna"
    assert str(coin2.to_dec_coin()) == "123456.789uluna"


def test_parse_int_coin():
    coin1 = Coin("uluna", 1001)
    coin2 = Coin.from_str("1001uluna")
    assert coin1 == coin2

    coin3 = Coin("uluna", -1)
    coin4 = Coin.from_str("-1uluna")
    assert coin3 == coin4


def test_parse_dec_coin():
    coin1 = Coin("uluna", 1001.5)
    coin2 = Coin.from_str("1001.500000000000000000uluna")
    assert coin1 == coin2

    coin3 = Coin("uluna", "-1.0")
    coin2 = Coin.from_str("-1.000000000000000000uluna")