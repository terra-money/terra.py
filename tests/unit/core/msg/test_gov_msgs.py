import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st
from hypothesis_jsonschema import from_schema

from terra_sdk.core.msg.gov import MsgDeposit, MsgSubmitProposal, MsgVote
from terra_sdk.core.sdk import Coin, Coins
from terra_sdk.error import InvalidAccAddress
from terra_sdk.util.validation import is_acc_address
from testtools import assert_serdes_consistent, assert_serdes_exact, load_msg_examples


@pytest.fixture(scope="module")
def msg_examples(tdd):
    """Stores the schema validation set for gov messages."""
    return load_msg_examples(tdd, msg_types=[MsgDeposit, MsgSubmitProposal, MsgVote],)


class TestMsgDeposit:
    def test_schema_valid(self, msg_examples):
        for m in msg_examples[MsgDeposit]:
            assert_serdes_consistent(MsgDeposit, m)
            assert_serdes_exact(MsgDeposit, m)

    @pytest.mark.serdes
    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(MsgDeposit.__schema__))
    def test_serdes_consistent(self, m):
        assert_serdes_consistent(MsgDeposit, m)

    def test_matches_meta(self):
        assert MsgDeposit.type == "gov/MsgDeposit"
        assert MsgDeposit.action == "deposit"

    @given(other=st.text())
    def test_constructor_validates_addresses(self, acc_address, other):
        """MsgDeposit should validate `depositor` to be AccAddress.
        """
        assume(not is_acc_address(other))
        with pytest.raises(InvalidAccAddress):
            MsgDeposit(proposal_id=1, depositor=other, amount=[])
        A = MsgDeposit(proposal_id=1, depositor=acc_address, amount=[])
        assert A.depositor == acc_address

    def test_constructor_canonizes_amount_to_coins(self, acc_address):
        """MsgDeposit should convert List[Coins] to sdk.Coins
        """
        amnt = [Coin("ukrw", 1000)]
        A = MsgDeposit(proposal_id=1, depositor=acc_address, amount=amnt)

        assert isinstance(A.amount, Coins)
        assert A.amount == amnt


class TestMsgSubmitProposal:
    def test_schema_valid(self, msg_examples):
        for m in msg_examples[MsgSubmitProposal]:
            assert_serdes_consistent(MsgSubmitProposal, m)
            # assert_serdes_exact(MsgSubmitProposal, m)
            # we can't have exact because serialize_to_json doesn't preserve key order.

    @pytest.mark.serdes
    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(MsgSubmitProposal.__schema__))
    def test_serdes_consistent(self, m):
        assert_serdes_consistent(MsgSubmitProposal, m)

    def test_matches_meta(self):
        assert MsgSubmitProposal.type == "gov/MsgSubmitProposal"
        assert MsgSubmitProposal.action == "submit_proposal"

    @given(other=st.text())
    def test_constructor_validates_addresses(self, acc_address, other):
        """MsgSubmitProposal should validate `proposer` to be AccAddress.
        """
        assume(not is_acc_address(other))
        with pytest.raises(InvalidAccAddress):
            MsgSubmitProposal(content=None, initial_deposit=[], proposer=other)
        A = MsgSubmitProposal(content=None, initial_deposit=[], proposer=acc_address)
        assert A.proposer == acc_address

    def test_constructor_canonizes_initial_deposit_to_coins(self, acc_address):
        """MsgSubmitProposal should convert initial_deposit List[Coins] to sdk.Coins
        """
        amnt = [Coin("ukrw", 1000)]
        A = MsgSubmitProposal(content=None, initial_deposit=amnt, proposer=acc_address)

        assert isinstance(A.initial_deposit, Coins)
        assert A.initial_deposit == amnt


class TestMsgVote:
    def test_schema_valid(self, msg_examples):
        for m in msg_examples[MsgVote]:
            assert_serdes_consistent(MsgVote, m)
            assert_serdes_exact(MsgVote, m)

    @pytest.mark.slow
    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(m=from_schema(MsgVote.__schema__))
    def test_serdes_consistent(self, m):
        assert_serdes_consistent(MsgVote, m)

    def test_matches_meta(self):
        assert MsgVote.type == "gov/MsgVote"
        assert MsgVote.action == "vote"

    @given(other=st.text())
    def test_constructor_validates_addresses(self, acc_address, other):
        """MsgVote should validate `voter` to be AccAddress."""
        assume(not is_acc_address(other))
        with pytest.raises(InvalidAccAddress):
            MsgVote(proposal_id=1, voter=other, option="")
        A = MsgVote(proposal_id=1, voter=acc_address, option="")
        assert A.voter == acc_address
