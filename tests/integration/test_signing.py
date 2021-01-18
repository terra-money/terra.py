"""Test suite translated from https://github.com/terra-project/terra-js/blob/master/tests/utils/txUtils.test.ts"""

import pytest

from terra_sdk import Terra
from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.core import (
    Coin,
    Coins,
    StdSignMsg,
    StdTx,
    StdFee,
    StdSignature,
    Input,
    Output,
)
from terra_sdk.core.msg import MsgSend, MsgMultiSend, MsgVote
from terra_sdk.util import hash_amino


@pytest.fixture
def terra():
    return Terra("columbus-3", "https://lcd.terra.dev")


@pytest.fixture
def master_key():
    return MnemonicKey(
        "island relax shop such yellow opinion find know caught erode blue dolphin behind coach tattoo light focus snake common size analyst imitate employ walnut"
    )


@pytest.fixture
def master_key2():
    return MnemonicKey(
        "spatial fantasy weekend romance entire million celery final moon solid route theory way hockey north trigger advice balcony melody fabric alter bullet twice push"
    )


@pytest.fixture
def a1():
    return MnemonicKey(
        "swamp increase solar renew twelve easily possible pig ostrich harvest more indicate lion denial kind target small dumb mercy under proud arrive gentle field"
    )


@pytest.fixture
def a2():
    return MnemonicKey(
        "service frozen keen unveil luggage initial surge name conduct mesh soup escape weather gas clown brand holiday result protect chat plug false pitch little"
    )


@pytest.fixture
def a3():
    return MnemonicKey(
        "corn peasant blue sight spy three stove confirm night brother vote dish reduce sick observe outside vacant arena laugh devote exotic wasp supply rally"
    )


def test_sign_tx(master_key):
    unsigned = StdSignMsg(
        msgs=[
            MsgSend(
                from_address=master_key.acc_address,
                to_address="terra1wg2mlrxdmnnkkykgqg4znky86nyrtc45q336yv",
                amount=[Coin("uluna", 100_000_000)],
            )
        ],
        sequence=0,
        account_number=45,
        chain_id="columbus-3-testnet",
        fee=StdFee(gas=46_467, amount=[Coin("uluna", 698)]),
    )
    signature = master_key.create_signature(unsigned)
    assert (
        signature.signature
        == "FJKAXRxNB5ruqukhVqZf3S/muZEUmZD10fVmWycdVIxVWiCXXFsUy2VY2jINEOUGNwfrqEZsT2dUfAvWj8obLg=="
    )


def test_multisig(a1, a2, a3):
    receiver = "terra1ptdx6akgk7wwemlk5j73artt5t6j8am08ql3qv"
    multisig = {
        "address": "terra16ddrexknvk2e443jsnle4n6s2ewjc6z3mjcu6d",
        "account_number": 46,
        "sequence": 0,
    }
    assert a1.acc_address == "terra12dazwl3yq6nwrce052ah3fudkarglsgvacyvl9"
    assert a2.acc_address == "terra1jqw25580qljucyy2xkpp7j02kd4mwx69wvfgf9"
    assert a3.acc_address == "terra13hrg8ul0p7sh85jwalh3leysdrw9swh44dql2h"

    send = MsgSend(
        from_address=multisig["address"],
        to_address=receiver,
        amount=[Coin("uluna", 100_000_000)],
    )

    unsigned = StdSignMsg(
        chain_id="columbus-3-testnet",
        account_number=multisig["account_number"],
        sequence=multisig["sequence"],
        msgs=[send],
        fee=StdFee.make(gas=50_000, uluna=750),
    )
    a1_sig = a1.create_signature(unsigned)
    assert (
        a1_sig.signature
        == "/kIFqGnmgOqMzf7guoe1eDTA1W5TjJcelJSRBdN0CTRyyxTMIbsxd+wL4fatHAq4hYOTf/zxD4l5xyU7/POZyg=="
    )
    a2_sig = a2.create_signature(unsigned)
    assert (
        a2_sig.signature
        == "hEjv9CnXQa89robHVsHS3GDZJiunnNb8xqziWD8D4aAuBXwxDzUXY14IE7q9Z3Qh0VMb3FBHuogHi7QZn2pM9g=="
    )
    a3_sig = a3.create_signature(unsigned)
    assert (
        a3_sig.signature
        == "CwHdmwC9ADtr5cTUdRZEfAcA8d1bgkF8fB+DcbB6MBB6amJz51WQYfVE1VgVTEY8Lyzg8+s8gX6nkqkXPeX72A=="
    )


def test_txid(terra):

    signature = StdSignature.from_data(
        {
            "signature": "+SnQyRQZ536m0VLTwWFn6WTlmV0ZP+EI08lIGbZFhvYMLPA+Dld3qaTFKwgJEd7kZrAb5OPWBUhiOc9326daEw==",
            "pub_key": {
                "type": "tendermint/PubKeySecp256k1",
                "value": "Ar+guke5UuM2XEZ9/ouPhAQbYs+f7y6jQCtGlI2lj1ZH",
            },
        }
    )

    # manually build TX
    tx = StdTx(
        msg=[
            MsgSend(
                from_address="terra1wg2mlrxdmnnkkykgqg4znky86nyrtc45q336yv",
                to_address="terra18h5pmhrz45z2ne7lz4nfd7cdfwl3jfeu99e7a5",
                amount=[Coin("uluna", 100_000_000)],
            )
        ],
        fee=StdFee.make(54_260, ukrw=814),
        signatures=[signature],
    )
    # get amino encoding
    amino = terra.tx.encode(tx)
    txhash = hash_amino(amino)
    assert txhash == "028b2acc80d244241114bf20b2982889201eca42bd400bc8f3a9d2162b5f0a3e"


def test_multisend(master_key2):
    """This test highlights how terra_sdk is flexible to accomodate many input styles."""

    multisend = MsgMultiSend(
        inputs=[
            Input(
                address=master_key2.acc_address,
                coins=[Coin("uluna", 1_000_000), Coin(denom="usdr", amount="1000000")],
            )
        ],
        outputs=[
            Output(
                "terra12dazwl3yq6nwrce052ah3fudkarglsgvacyvl9", [Coin("uluna", 500000)]
            ),
            {
                "address": "terra1ptdx6akgk7wwemlk5j73artt5t6j8am08ql3qv",
                "coins": Coins() + Coin("uluna", 500000) + Coin("usdr", 1000000),
            },
        ],
    )

    unsigned = StdSignMsg(
        account_number=47,
        sequence=0,
        chain_id="columbus-3-testnet",
        msgs=[multisend],
        fee=StdFee.make(100_000, uluna=1500, usdr=1000),
        memo="1234",
    )

    tx = master_key2.sign_tx(unsigned)

    assert (
        tx.signatures[0].signature
        == "YA/ToXLxuuAOQlpm5trbIUu2zv5NfBmeHz2jmXgNrt8jP+odukerfri3DUXAJuhETAMHVVV78t7Q4xC0j+CVkA=="
    )


def test_vote(terra):
    vote = MsgVote(
        proposal_id=1,
        voter="terra1wg2mlrxdmnnkkykgqg4znky86nyrtc45q336yv",
        option=MsgVote.YES,
    )

    signature = StdSignature.from_data(
        {
            "signature": "Xn93OEY/HYXxE2rqL6O5Cj0r/D+GbaPxEgvKM+hMFQJA/95RE4dLPJdLP5HpmeLrBm46GI0V6w27pR1Pq4mH+g==",
            "pub_key": {
                "type": "tendermint/PubKeySecp256k1",
                "value": "Ar+guke5UuM2XEZ9/ouPhAQbYs+f7y6jQCtGlI2lj1ZH",
            },
        }
    )

    tx = StdTx(msg=[vote], fee=StdFee.make(70_000, uluna=1050), signatures=[signature])

    amino = terra.tx.encode(tx)
    txhash = hash_amino(amino)

    assert txhash == "f1af6a4193c500578a457dd68ee34131e15d8e1c462bba647c43e882fcd74e57"
