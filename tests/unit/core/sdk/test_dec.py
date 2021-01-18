from decimal import Decimal

import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st
from hypothesis_jsonschema import from_schema

from terra_sdk.core import Dec
from testtools import assert_serdes_consistent, assert_serdes_exact

dec_input = st.one_of(
    st.integers(),
    st.floats(
        allow_infinity=False,
        allow_nan=False,
        min_value=-(10 ** 18),
        max_value=10 ** 18,
    ),
    st.decimals(
        allow_infinity=False,
        allow_nan=False,
        min_value=-(10 ** 25),
        max_value=10 ** 25,
        places=18,
    ),
    from_schema(Dec.__schema__),
)


@pytest.fixture(scope="module")
def inc():
    nd = Dec(0)
    nd.i = 1
    return nd


@pytest.mark.sdk
class TestDecSerdes:
    @pytest.mark.serdes
    @given(d=from_schema(Dec.__schema__))
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    def test_serdes_consistent(self, d):
        assert_serdes_consistent(Dec, d)

    def test_simple_check(self):
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
        for x in examples:
            assert str(Dec(x)) == x

    def test_serializes_zero(self):
        Z = "0.000000000000000000"
        assert str(Dec(0)) == Z
        assert str(Dec("0")) == Z
        assert str(Dec("-0")) == Z
        assert str(Dec("-00")) == Z
        assert str(Dec("-00.0")) == Z
        assert str(Dec("-00.0000000000000000000232")) == Z

    def test_serializes_18_digits(self):
        examples = [
            ("0.5", "0.500000000000000000"),
            ("0.00625", "0.006250000000000000"),
            ("3913.11", "3913.110000000000000000"),
            ("-23.11", "-23.110000000000000000"),
            ("3", "3.000000000000000000"),
            ("-3", "-3.000000000000000000"),
        ]
        for x in examples:
            assert str(Dec(x[0])) == x[1]

    def test_str_regex(self):
        """`Dec` will only parse strings that match Decimal format: `/^(\-)?(\d+)(\.\d+)?\Z/`
        """
        bad_examples = [
            "a1.2",
            "..2",
            "0b00",
            "0xdeadb33f",
            "0.0.5",
            "(626)112-3322",
            "2.14E-14",
            "42.",
            ".420",
        ]
        for bad in bad_examples:
            with pytest.raises(ValueError):
                Dec(bad)

        good_examples = [
            "0.0",
            "42.0",
            "333333.213123923402394",
            "1127.10102392039129301293230921039",
            "13123891823912839123.239482934829348239489",
            "-239299920",
            "-0000.0",
        ]
        for good in good_examples:
            assert isinstance(Dec(good).i, int)

    @given(x=st.integers())
    def test_serializes_int_into_dec(self, x):
        """`Dec` should capture simple `ints` and serialize it to 18 digits
        of precision.
        """
        A = str(x)
        assert str(Dec(A)) == A + "." + 18 * "0"

    @given(
        x=st.decimals(
            allow_infinity=False,
            allow_nan=False,
            min_value=-(10 ** 18),
            max_value=10 ** 18,
            places=18,
        )
    )
    def test_converts_decimal_objects(self, x):
        """`Dec` should capture a compatible `Decimal` object and serialize
        to 18 digits of precision.
        """
        d = Dec(x)
        r = str(d).split(".")
        if x < 0:
            assert d.i < 0
        assert int(r[0]) == int(x)
        assert len(r[1]) == 18

    @given(x=st.integers(), y=st.integers(18, 99))
    def test_truncates_beyond_18_digits(self, x, y):
        """If Dec is provided a string representing a number with higher
        degree of precision than 18 digits, those extra digits should be truncated.
        """
        A = str(x) + "." + y * "7"
        r = str(Dec(A)).split(".")
        assert r[0] == str(x)
        assert len(r[1]) == 18

    @pytest.mark.slow
    @given(x=dec_input)
    def test_constructor_copies(self, x):
        """Dec should copy another Dec in the constructor, and the resulting
        object should be equivalent but not share the same address in memory.
        """
        A = Dec(x)
        B = Dec(A)
        assert A == B
        assert A is not B


@pytest.mark.sdk
class TestDecOperations:
    @pytest.mark.slow
    @given(x=dec_input)
    def test_int(self, x):
        if isinstance(x, str) and "." in x:
            x = x.split(".")[0]
        input_int = int(x)
        output_int = int(Dec(x))
        assert output_int == input_int

    @pytest.mark.slow
    @given(x=dec_input)
    def test_equality_consistent(self, x):
        assert Dec(x) == Dec(x)

    @given(x=st.integers())
    def test_equality_integer(self, x):
        assert Dec(x) == x

    def test_equality_float(self):
        # NOTE: This is about the limit of how robust it is for float
        # In the future, perhaps remove support for float due to lack of utility.
        assert Dec(1.2) == 1.2
        assert Dec(2342.123232) == 2342.123232
        assert Dec(2342.123232123) == 2342.123232123

    def test_equality_decimal(self):
        assert Dec(Decimal("1.45")) == Decimal("1.45")
        assert Dec(Decimal("2342.123232123")) == Decimal("2342.123232123")
        assert Dec(Decimal("2332423442.123234234232123")) == Decimal(
            "2332423442.123234234232123"
        )
        # 24, 18 digit decimal precision
        assert Dec(Decimal("423412312312312342123123.123234234232123123")) == Decimal(
            "423412312312312342123123.123234234232123123"
        )
        # disregard beyond 19 digits of precision
        assert Dec(Decimal("0.1232342342321231233")) == Decimal("0.1232342342321231233")

    @pytest.mark.slow
    @given(x=dec_input, y=dec_input)
    def test_lt_gt(self, x, y):
        assume(not isinstance(x, str) and not isinstance(y, str) and x < y)
        assert Dec(x) < Dec(y)
        assert Dec(y) > Dec(x)
        assert not Dec(x) > Dec(x)
        assert not Dec(x) < Dec(x)
        assert Dec(x) >= Dec(x)
        assert Dec(x) <= Dec(x)
        assert Dec(x) <= Dec(y)
        assert Dec(y) >= Dec(x)

    @pytest.mark.slow
    @given(x=dec_input)
    def test_neg(self, x):
        assume(not isinstance(x, str))
        assert -Dec(x) == Dec(-x)

    @given(x=dec_input)
    def test_abs(self, x):
        assert abs(Dec(x)) >= 0

    @pytest.mark.slow
    @pytest.mark.parametrize("zero", [0, 0.0, Decimal(0), Dec(0)])
    @given(x=dec_input, y=dec_input)
    def test_add_properties(self, x, y, zero):
        assume(x != y)
        assert Dec(x) + 0 == Dec(x)
        assert Dec(x) + 0 == 0 + Dec(x)
        assert Dec(x) + Dec(y) == Dec(y) + Dec(x)
        if not isinstance(x, str) and not isinstance(y, str):
            assert Dec(x) + y == y + Dec(x)
            assert isinstance(Dec(x) + y, Dec)
            assert isinstance(y + Dec(x), Dec)
        if isinstance(x, int) and isinstance(y, int):
            assert Dec(x) + Dec(y) == Dec(x + y)

    def test_add(self, inc):
        assert inc + inc == Dec("0.000000000000000002")
        assert (inc + inc).i == 2

    @pytest.mark.slow
    @pytest.mark.parametrize("zero", [0, 0.0, Decimal(0), Dec(0)])
    @given(x=dec_input, y=dec_input)
    def test_sub_properties(self, x, y, zero):
        assert Dec(x) - zero == Dec(x)
        assert Dec(x) - Dec(y) == -Dec(y) + Dec(x)
        assert Dec(x) - Dec(x) == zero
        assert isinstance(Dec(x) - Dec(y), Dec)
        if not isinstance(y, str):
            assert Dec(x) - y == -y + Dec(x)
            assert isinstance(Dec(x) - y, Dec)
            assert isinstance(y - Dec(x), Dec)
        if isinstance(x, int) and isinstance(y, int):
            assert Dec(x) - Dec(y) == Dec(x - y)

    @pytest.mark.slow
    @pytest.mark.parametrize("one", [1, 1.0, Decimal(1), Dec(1)])
    @given(x=dec_input, y=dec_input)
    def test_mul_properties(self, x, y, one):
        assume(x != y)
        assert Dec(x) * one == Dec(x)
        assert Dec(x) * one == one * Dec(x)
        assert Dec(x) * Dec(y) == Dec(y) * Dec(x)
        if not isinstance(x, str) and not isinstance(y, str):
            assert Dec(x) * y == y * Dec(x)
            assert isinstance(Dec(x) * y, Dec)
            assert isinstance(y * Dec(x), Dec)
        if isinstance(x, int) and isinstance(y, int):
            assert Dec(x) * Dec(y) == Dec(x * y)

    def test_mul_examples(self):
        # TODO: add better examples
        examples = [
            (Dec("6.3") * Dec("6.5"), Dec("40.95")),
            (Dec("27.37") * Dec("36.299"), Dec("993.50363")),
            (Dec("-5231.234232") * 5.5, Dec("-28771.788276")),
        ]
        for x in examples:
            assert x[0] == x[1]

    # TODO: add tests for truediv, floordiv
    def test_cosmos_quo(self):
        examples = [
            (Dec(-1), Dec(-1), Dec(1)),
            (Dec(3), Dec(7), Dec.with_prec(428571428571428571, 18)),
            (
                Dec.with_prec(3333, 4),
                Dec.with_prec(333, 4),
                Dec("10.009009009009009009"),
            ),
        ]
        for x in examples:
            assert x[0] / x[1] == x[2]

    def test_cosmos_mul(self):
        examples = [
            (Dec(-1), Dec(-1), Dec(1)),
            (Dec(3), Dec(7), Dec(21)),
            (Dec.with_prec(3333, 4), Dec.with_prec(333, 4), Dec.with_prec(1109889, 8),),
        ]
        for x in examples:
            assert x[0] * x[1] == x[2]

    def test_cosmos_overflow(self):
        """Analog for this test:
        https://github.com/cosmos/cosmos-sdk/blob/5a2e59ebb23d1d23546f1145d8814a457655935a/types/decimal_test.go#L334
        """
        a = Dec("51643150036226787134389711697696177267")
        b = Dec("-31798496660535729618459429845579852627")
        assert str(a + b) == "19844653375691057515930281852116324640.000000000000000000"
