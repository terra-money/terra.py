""" done
import lcd_auth
import lcd_authz
import lcd_bank
import lcd_distribution
import lcd_gov
import lcd_market
import lcd_mint
import lcd_oracle
import lcd_slashing
import lcd_wasm
import lcd_treasury
import lcd_tendermint
import lcd_ibc
import lcd_ibc_transfer

"""

from terra_sdk.client.lcd import LCDClient

# import lcd_tx
from terra_sdk.client.lcd.api.tx import CreateTxOptions, SignerOptions
from terra_sdk.client.localterra import LocalTerra
from terra_sdk.core.bank import MsgMultiSend, MsgSend, MultiSendInput, MultiSendOutput
from terra_sdk.core.tx import SignMode
from terra_sdk.key.key import SignOptions
from terra_sdk.util.json import JSONSerializable

""" untested
import lcd_gov
"""

########

from terra_sdk.core import Coin, Coins, SignDoc
from terra_sdk.core.public_key import SimplePublicKey


def main():
    terra = LocalTerra()
    wallet1 = terra.wallets["test1"]
    wallet2 = terra.wallets["test2"]
    info1 = wallet1.account_number_and_sequence()
    info2 = wallet2.account_number_and_sequence()

    inputs = [
        MultiSendInput(
            address=wallet1.key.acc_address,
            coins=Coins(uluna=10000),
        ),
        MultiSendInput(
            address=wallet2.key.acc_address,
            coins=Coins(uluna=20000),
        )
    ]
    outputs = [
        MultiSendOutput(
            address=wallet2.key.acc_address,
            coins=Coins(uluna=10000),
        ),
        MultiSendOutput(
            address=wallet1.key.acc_address,
            coins=Coins(uluna=20000),
        ),
    ]

    msg = MsgMultiSend(inputs, outputs)

    opt = CreateTxOptions(
        msgs=[msg]
    )

    tx = terra.tx.create(
        [SignerOptions(
            address=wallet1.key.acc_address,
            sequence=info1["sequence"],
            public_key=wallet1.key.public_key
        ), SignerOptions(
            address=wallet2.key.acc_address,
            sequence = info2["sequence"],
            public_key = wallet2.key.public_key
        )],
        opt
    )


    signdoc1 = SignDoc(
        chain_id=terra.chain_id,
        account_number=info1["account_number"],
        sequence=info1["sequence"],
        auth_info=tx.auth_info,
        tx_body=tx.body,
    )

    signdoc2 = SignDoc(
        chain_id=terra.chain_id,
        account_number=info2["account_number"],
        sequence=info2["sequence"],
        auth_info=tx.auth_info,
        tx_body=tx.body,
    )
    sig1 = wallet1.key.create_signature_amino(signdoc1)
    sig2 = wallet2.key.create_signature_amino(signdoc2)
    tx.append_signatures([sig1, sig2])

    print(msg.to_amino())

    result = terra.tx.broadcast(tx)
    print(f"RESULT:{result}")


main()
