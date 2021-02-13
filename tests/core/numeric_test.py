import pytest

from terra_sdk.core import Dec


def test_deserializes():
    examples = [
        "138875042105.980753034749566779",
        "8447.423744387144096286",
        "3913.113789811986907029",
        "0.500000000000000000",
        "0.006250000000000000",
        "-23.128250000000000023",
        "242.000000000000028422",
        "-242.000000000000020422",
    ]

    for example in examples:
        assert str(Dec(example)) == example


def test_zero():
    zero = Dec("0")
    assert str(zero) == "0.000000000000000000"


def test_18_digits_of_precision():
    examples = [
        ["0.5", "0.500000000000000000"],
        ["0.00625", "0.006250000000000000"],
        ["3913.11", "3913.110000000000000000"],
        ["-23.11", "-23.110000000000000000"],
        ["-3", "-3.000000000000000000"],
        ["-3.0000000000000000001", "-3.000000000000000000"],
    ]

    for (example, expected) in examples:
        assert str(Dec(example)) == expected


def test_add_sub_resolution():
    zero = Dec("0")
    unit = Dec("0.000000000000000001")
    assert zero.add(unit) == unit
    assert zero.sub(unit) == unit.mul(-1)


@pytest.mark.parametrize(
    "d1,d2,mul,quo,add,sub",
    [
        [Dec(0), Dec(1), Dec(0), Dec(0), Dec(1), Dec(-1)],
        [Dec(0), Dec(-1), Dec(-0), Dec(0), Dec(-1), Dec(1)],
        [
            Dec(3),
            Dec(7),
            Dec(21),
            Dec.with_prec("428571428571428571", 18),
            Dec(10),
            Dec(-4),
        ],
        [Dec(2), Dec(4), Dec(8), Dec.with_prec(5, 1), Dec(6), Dec(-2)],
        [Dec(100), Dec(100), Dec(10000), Dec(1), Dec(200), Dec(0)],
        [
            Dec.with_prec(15, 1),
            Dec.with_prec(15, 1),
            Dec.with_prec(225, 2),
            Dec(1),
            Dec(3),
            Dec(0),
        ],
        [
            Dec.with_prec(3333, 4),
            Dec.with_prec(333, 4),
            Dec.with_prec(1109889, 8),
            Dec("10.009009009009009009"),
            Dec.with_prec(3666, 4),
            Dec.with_prec(3, 1),
        ],
    ],
)
def test_cosmos_arithmetic(d1, d2, mul, quo, add, sub):
    assert d1.mul(d2) == mul
    assert d1 * d2 == mul
    assert d1.div(d2) == quo
    assert d1 / d2 == quo
    assert d1.add(d2) == add
    assert d1 + d2 == add
    assert d1.sub(d2) == sub
    assert d1 - d2 == sub
