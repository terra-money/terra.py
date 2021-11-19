import asyncio
import base64
from pathlib import Path

from terra_sdk.client.lcd.api.tx import CreateTxOptions, SignerOptions
from terra_sdk.client.localterra import LocalTerra
from terra_sdk.core import Coins, LegacyAminoPubKey, MultiSignature, SignatureV2, SignDoc
from terra_sdk.core.bank import MsgSend
from terra_sdk.util.contract import get_code_id


def main():
    terra = LocalTerra()
    test1 = terra.wallets["test1"]
    test2 = terra.wallets["test2"]
    test3 = terra.wallets["test3"]

    multisigPubKey = LegacyAminoPubKey(2, [test1.key, test2.key, test3.key])

    address = multisigPubKey.address()
    multisig = MultiSignature(multisigPubKey)

    msg = MsgSend(
        address,
        "terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp",
        Coins(uluna=1000000),
    )

    accInfo = terra.auth.account_info(address)
    tx = terra.tx.create(
        signers=SignerOptions(
            address=address,
            sequence=accInfo.get_sequence(),
            public_key=accInfo.get_public_key()
        ),
        options=CreateTxOptions(
            msgs=[msg],
            memo='multisig test',
            gas_prices="0.2uluna",
            gas_adjustment=1.5
        )
    )
    signDoc = SignDoc(
        chain_id=terra.chain_id,
        account_number=accInfo.get_account_number(),
        sequence=accInfo.get_sequence(),
        auth_info=tx.auth_info,
        tx_body=tx.body
    )

    sig1 = test1.key.create_signature_amino(signDoc)
    sig2 = test2.key.create_signature_amino(signDoc)

    multisig.append_signature_v2s([sig1, sig2])
    sig_v2 = SignatureV2(public_key=multisigPubKey,
                         data=multisig.to_signature_descriptor(),
                         sequence=accInfo.get_sequence())
    tx.append_signatures([sig_v2])

    print("-"*32)
    print(tx.to_data())
    print("-"*32)
    result = terra.tx.broadcast(tx)
    print(result)


main()
