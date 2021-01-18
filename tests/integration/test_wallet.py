import pytest

from terra_sdk import Terra
from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.core.sdk.coin import Coins
from terra_sdk.core.msg.bank import MsgSend
from terra_sdk.error import TxError
from terra_sdk.core.auth.transaction import TxBroadcastResult


@pytest.fixture
def msg(wallet, mnemonics):
    recipient = mnemonics[2]["address"]
    return MsgSend(
        from_address=wallet.address, to_address=recipient, amount=Coins(uluna=1)
    )


class TestWallet:
    """Tests wallet transaction features."""

    def test_account_number(self, wallet):
        assert wallet.account_number == 189

    def test_sequence(self, wallet, msg, fee):
        """Sequence should increment after a transaction."""
        seq = wallet.sequence
        tx = wallet.create_and_sign_tx(msg, fee=fee)
        wallet.broadcast(tx)
        assert wallet.sequence == seq + 1

    def test_multiple_tx(self, wallet, msg):
        """Multiple TX's generated should have the same sequence number because the
        sequence number is live-fetched from the blockchain each time."""
        seq = wallet.sequence
        tx1 = wallet.create_tx(msg)
        tx2 = wallet.create_tx(msg)
        tx3 = wallet.create_tx(msg)

        assert tx1.sequence == seq
        assert tx2.sequence == seq
        assert tx3.sequence == seq

    def test_manual(self, wallet, msg):
        """Wallet can be used in manual-incrementing mode context, where the automatic
        fetching of sequence is paused for tx generation."""
        seq = wallet.sequence
        with wallet.manual() as w:
            tx1 = w.create_tx(msg)
            tx2 = w.create_tx(msg)
            _ = w.create_and_sign_tx(msg)  # make stdtx, and sequence is not known
            tx4 = w.create_tx(msg)
            assert w.sequence == seq  # wallet.sequence behavior should not change
            # this only applies to creating TX behavior.
        assert tx1.sequence == seq
        assert tx2.sequence == seq + 1
        assert tx4.sequence == seq + 3
        assert wallet.sequence == seq

        tx_after = wallet.create_tx(msg)
        tx_after_2 = wallet.create_tx(msg)

        # normal behavior should resume.
        assert tx_after.sequence == seq
        assert tx_after_2.sequence == seq

    def test_new_wallet_send(self, terra, wallet, fee):
        """A new wallet should be able to make transactions."""

        new_wallet = terra.wallet(MnemonicKey.generate())
        send = MsgSend(
            from_address=new_wallet.address,
            to_address=wallet.address,
            amount=Coins(uluna=1),
        )
        tx = new_wallet.create_and_sign_tx(send, fee=fee)
        with pytest.raises(TxError):
            new_wallet.broadcast(tx)

        tx = wallet.create_and_sign_tx(
            MsgSend(
                from_address=wallet.address,
                to_address=new_wallet.address,
                amount=Coins(uluna=10000000),
            ),
            fee=fee,
        )
        wallet.broadcast(tx)
        tx = new_wallet.create_and_sign_tx(send, fee=fee)
        res = new_wallet.broadcast(tx)
        assert isinstance(res, TxBroadcastResult)
