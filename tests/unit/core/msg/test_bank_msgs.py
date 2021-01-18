import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st
from hypothesis_jsonschema import from_schema

from terra_sdk.core.bank import Input, Output
from terra_sdk.core.msg.bank import MsgMultiSend, MsgSend
from terra_sdk.core.sdk import Coin, Coins
from terra_sdk.error import InvalidAccAddress
from terra_sdk.util.validation import is_acc_address
from testtools import assert_serdes_consistent, assert_serdes_exact, load_msg_examples


@pytest.fixture(scope="module")
def msg_examples(tdd):
    """Stores the __schema__ validation set for slashing messages."""
    return load_msg_examples(tdd, msg_types=[MsgSend, MsgMultiSend],)


@pytest.fixture
def dict_list(acc_address):
    return [
        {"address": acc_address, "coins": []},
        {"address": acc_address, "coins": []},
    ]


@pytest.fixture
def input_list(acc_address):
    return [
        Input(address=acc_address, coins=[]),
        Input(address=acc_address, coins=[]),
    ]


@pytest.fixture
def output_list(acc_address):
    return [
        Output(address=acc_address, coins=[]),
        Output(address=acc_address, coins=[]),
    ]


@pytest.fixture
def mixed_list(acc_address):
    return [
        Output(address=acc_address, coins=[]),
        Input(address=acc_address, coins=[]),
        {"address": acc_address, "coins": []},
    ]


@pytest.fixture
def input_list_with_dict(acc_address):
    return [
        Input(address=acc_address, coins=[]),
        {"address": acc_address, "coins": []},
    ]


@pytest.fixture
def output_list_with_dict(acc_address):
    return [
        Output(address=acc_address, coins=[]),
        {"address": acc_address, "coins": []},
    ]


class TestMsgSend:
    def test_schema_valid(self, msg_examples):
        for m in msg_examples[MsgSend]:
            assert_serdes_consistent(MsgSend, m)
            assert_serdes_exact(MsgSend, m)

    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(MsgSend.__schema__))
    def test_serdes_consistent(self, m):
        assert_serdes_consistent(MsgSend, m)

    def test_matches_meta(self):
        assert MsgSend.type == "bank/MsgSend"
        assert MsgSend.action == "send"

    @given(other=st.text())
    def test_constructor_validates_addresses(self, acc_address, other):
        """MsgSend should validate both from_address and to_address to be AccAddress.
        """

        assume(not is_acc_address(other))

        with pytest.raises(InvalidAccAddress):
            MsgSend(from_address=acc_address, to_address=other, amount=[])
        with pytest.raises(InvalidAccAddress):
            MsgSend(from_address=other, to_address=acc_address, amount=[])

        A = MsgSend(from_address=acc_address, to_address=acc_address, amount=[])
        assert A.from_address == acc_address

    def test_constructor_amount_canonizes_list_to_coins(self, acc_address):
        """Creating a MsgSend object directly through its constructor should be conveniently
        achievable with either a sdk.Coins object or List[Coin].
        """

        c = [Coin("uluna", 130000), Coin("ukrw", 12000000)]
        A = MsgSend(from_address=acc_address, to_address=acc_address, amount=c)
        B = MsgSend(from_address=acc_address, to_address=acc_address, amount=Coins(c))

        assert A == B

        C = MsgSend(from_address=acc_address, to_address=acc_address, amount=[])
        D = MsgSend(from_address=acc_address, to_address=acc_address, amount=Coins())

        assert C == D

        assert isinstance(A.amount, Coins)
        assert isinstance(C.amount, Coins)


class TestMsgMultiSend:
    def test_schema_valid(self, msg_examples):
        for m in msg_examples[MsgMultiSend]:
            assert_serdes_consistent(MsgMultiSend, m)
            assert_serdes_exact(MsgMultiSend, m)

    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(MsgMultiSend.__schema__))
    def test_serdes_consistent(self, m):
        assert_serdes_consistent(MsgMultiSend, m)

    def test_matches_meta(self):
        assert MsgMultiSend.type == "bank/MsgMultiSend"
        assert MsgMultiSend.action == "multisend"

    @given(other=st.text())
    def test_constructor_validates_addresses(self, acc_address, dict_list, other):
        """MsgMultiSend should validate inputs[x].address and outputs[x].address if inputs and outputs
        are passed in as dicts.
        """
        assume(not is_acc_address(other))

        bad = [{"address": acc_address, "coins": []}, {"address": other, "coins": []}]
        with pytest.raises(InvalidAccAddress):
            MsgMultiSend(inputs=bad, outputs=dict_list)
        with pytest.raises(InvalidAccAddress):
            MsgMultiSend(inputs=dict_list, outputs=bad)
        with pytest.raises(InvalidAccAddress):
            MsgMultiSend(inputs=bad, outputs=bad)

        A = MsgMultiSend(inputs=dict_list, outputs=dict_list)

    def test_constructor_takes_io_or_list_dict(
        self, input_list_with_dict, output_list_with_dict, input_list, output_list
    ):
        """MsgMultiSend should accept either list of Input/Output objects or {address: ..., coins: Coins},
        which should be treated as interoperable.
        """
        A = MsgMultiSend(inputs=input_list_with_dict, outputs=output_list_with_dict)
        B = MsgMultiSend(inputs=input_list, outputs=output_list)

        assert A == B

    def test_constructor_canonizes_dict_to_io(
        self, input_list_with_dict, output_list_with_dict, dict_list
    ):
        """MsgMultiSend should use Input/Output internally, regardless of whether the
        `inputs` or `outputs` were passed as dicts.
        """

        A = MsgMultiSend(inputs=input_list_with_dict, outputs=output_list_with_dict)
        B = MsgMultiSend(inputs=dict_list, outputs=dict_list)

        assert all(isinstance(i, Input) for i in A.inputs)
        assert all(isinstance(o, Output) for o in A.outputs)

    def test_constructor_checks_inputs_outputs(
        self, mixed_list, input_list, output_list, dict_list,
    ):
        """MsgMultiSend should prevent instatiation if an Input is passed into the output, or
        vice-versa.
        """

        with pytest.raises(TypeError):
            MsgMultiSend(inputs=mixed_list, outputs=output_list)
        with pytest.raises(TypeError):
            MsgMultiSend(inputs=input_list, outputs=mixed_list)
        with pytest.raises(TypeError):
            MsgMultiSend(inputs=output_list, outputs=output_list)
        with pytest.raises(TypeError):
            MsgMultiSend(inputs=input_list, outputs=input_list)

        A = MsgMultiSend(inputs=input_list, outputs=output_list)
        B = MsgMultiSend(inputs=dict_list, outputs=dict_list)

        assert A == B

        assert all(isinstance(i, Input) for i in A.inputs)
        assert all(isinstance(o, Output) for o in A.outputs)
        assert all(isinstance(i, Input) for i in B.inputs)
        assert all(isinstance(o, Output) for o in B.outputs)
