import pytest

from terra_sdk import Terra
from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.core.msg import *
from terra_sdk.core import StdFee, Coin, Dec, Coins
from terra_sdk.error import CodespaceError, TxCodespaceError
from terra_sdk.core.proposal import *
from terra_sdk.core.treasury import PolicyConstraints


class TestTx:
    def test_broadcast(self, wallet, fee):
        swap = MsgSwap(
            trader=wallet.address, offer_coin=Coin("uluna", 1), ask_denom="umnt"
        )
        tx = wallet.create_and_sign_tx(swap, fee=fee)
        res = wallet.broadcast(tx)
        assert res.msgs is not None

    def test_broadcast_txcodespacerror(self, wallet, fee, mnemonics):
        """Tests that a that it captures the correct txcodespace error."""
        fail_swap = MsgSwap(
            trader=wallet.address, offer_coin=Coin("uluna", 1), ask_denom="bebo"
        )
        fail_vote = MsgExchangeRateVote(
            exchange_rate="603.899000000000000000",
            salt="0dff",
            denom="umnt",
            feeder=wallet.address,
            validator="terravaloper1vqnhgc6d0jyggtytzqrnsc40r4zez6tx99382w",
        )
        send = MsgSend(
            from_address=wallet.address,
            to_address=mnemonics[1]["address"],
            amount=Coins(uluna=1),
        )

        tx1 = wallet.create_and_sign_tx(send, send, fail_swap, send, fail_vote, fee=fee)
        with pytest.raises(TxCodespaceError) as excinfo:
            wallet.broadcast(tx1)
        err = excinfo.value
        assert err.codespace == "market"

        tx2 = wallet.create_and_sign_tx(
            send, fail_vote, send, send, fail_swap, fail_swap, fee=fee
        )
        with pytest.raises(TxCodespaceError) as excinfo:
            wallet.broadcast(tx2)
        err = excinfo.value
        assert err.codespace == "oracle"

    def test_make_proposal(self, wallet, fee):
        e = MsgSubmitProposal(
            content=ParameterChangeProposal(
                "testing params",
                "yay!",
                changes={
                    "distribution": {
                        "community_tax": Dec(0),
                        "base_proposer_reward": Dec(32),
                        "bonus_proposer_reward": Dec(22),
                        "withdraw_addr_enabled": True,
                    },
                    "staking": {
                        "unbonding_time": 33,
                        "max_validators": 9999,
                        "max_entries": 2323,
                        "bond_denom": "uluna",
                    },
                    "slashing": {
                        "max_evidence_age": 234234,
                        "signed_blocks_window": 1,
                        "min_signed_per_window": Dec(1),
                        "downtime_jail_duration": 1,
                        "SlashFractionDoubleSign": Dec(100),
                        "slash_fraction_downtime": Dec(213.123),
                    },
                    "treasury": {
                        "tax_policy": PolicyConstraints(
                            rate_min=Dec(0),
                            rate_max=Dec(100),
                            cap=Coin("unused", 0),
                            change_max=Dec(3),
                        ),
                        "reward_policy": PolicyConstraints(
                            rate_min=Dec(0),
                            rate_max=Dec(1023423340),
                            cap=Coin("unused", 0),
                            change_max=Dec(3),
                        ),
                        "seigniorage_burden_target": Dec("2342.234234"),
                        "mining_increment": Dec(23423423423.234234234234982),
                        "window_short": 50,
                        "window_long": 2,
                        "window_probation": 30,
                    },
                    "oracle": {
                        "vote_period": 345345,
                        "vote_threshold": Dec("2342.234333"),
                        "reward_band": Dec("234343"),
                        "reward_distribution_window": 345345,
                        "whitelist": ["abc", "bdc", "ttt"],
                        "slash_fraction": Dec(23423.232343),
                        "slash_window": 343311,
                        "min_valid_per_window": Dec(2342.234234),
                    },
                    "market": {
                        "pool_recovery_period": 234234234,
                        "base_pool": Dec(232323232),
                        "min_spread": Dec(343434),
                        "illiquid_tobin_tax_list": [{"denom": "item", "msg": "sdfsdf"}],
                    },
                    "gov": {
                        "deposit_params": {
                            "min_deposit": Coins(uluna=2, ukrw=5),
                            "max_deposit_period": 30434,
                        },
                        "voting_params": {"voting_period": 434243234},
                        "tallyparams": {
                            "quorum": Dec(234234.2334),
                            "threshold": Dec(23423.2323),
                            "veto": Dec(1232.234),
                        },
                    },
                },
            ),
            initial_deposit=Coins(uluna=10000000),
            proposer=wallet.address,
        )
        print(wallet.address)
        print(wallet.account_number, wallet.sequence)
        tx = wallet.create_and_sign_tx(e, fee=fee)
        res = wallet.broadcast(tx)

