from terra_sdk.core.auth import StdFee, StdSignMsg
from terra_sdk.core.bank import MsgSend
from terra_sdk.key.mnemonic import MnemonicKey


def test_derivation():
    mk = MnemonicKey(
        "wonder caution square unveil april art add hover spend smile proud admit modify old copper throw crew happy nature luggage reopen exhibit ordinary napkin"
    )
    assert mk.acc_address == "terra1jnzv225hwl3uxc5wtnlgr8mwy6nlt0vztv3qqm"
    assert (
        mk.acc_pubkey
        == "terrapub1addwnpepqt8ha594svjn3nvfk4ggfn5n8xd3sm3cz6ztxyugwcuqzsuuhhfq5nwzrf9"
    )
    assert mk.val_address == "terravaloper1jnzv225hwl3uxc5wtnlgr8mwy6nlt0vztraasg"
    assert (
        mk.val_pubkey
        == "terravaloperpub1addwnpepqt8ha594svjn3nvfk4ggfn5n8xd3sm3cz6ztxyugwcuqzsuuhhfq5y7accr"
    )


def test_random():
    mk1 = MnemonicKey()
    mk2 = MnemonicKey()
    assert mk1.mnemonic != mk2.mnemonic


def test_signature():
    mk = MnemonicKey(
        "island relax shop such yellow opinion find know caught erode blue dolphin behind coach tattoo light focus snake common size analyst imitate employ walnut"
    )

    send = MsgSend(
        mk.acc_address,
        "terra1wg2mlrxdmnnkkykgqg4znky86nyrtc45q336yv",
        dict(uluna="100000000"),
    )

    fee = StdFee(46467, dict(uluna=698))

    stdsignmsg = StdSignMsg("columbus-3-testnet", 45, 0, fee, [send], "")
    signature = mk.create_signature(stdsignmsg).signature
    assert (
        signature
        == "FJKAXRxNB5ruqukhVqZf3S/muZEUmZD10fVmWycdVIxVWiCXXFsUy2VY2jINEOUGNwfrqEZsT2dUfAvWj8obLg=="
    )
