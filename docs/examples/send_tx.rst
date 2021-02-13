Sending assets
==============

The following example tries to send 1 LUNA and 1 KRT to the recipient of your choice.

.. code-block:: python

    from terra_sdk.client.lcd import LCDClient
    from terra_sdk.core.bank import MsgSend
    from terra_sdk.core import Coins
    from terra_sdk.key.mnemonic import MnemonicKey

    MNEMONIC = "<your-mnemonic>"
    RECIPIENT = "<recipient-address"

    # make a Key instance from our mnemonic
    mk = MnemonicKey(mnemonic=MNEMONIC)

    # represents our connection to the node
    terra = LCDClient(
        url="https://lcd.terra.dev",
        chain_id="columbus-4"
    )

    # a wallet object helps you build and sign transactions
    wallet = terra.wallet(mk)

    # message tells the blockchain what to change
    send_msg = MsgSend(
        wallet.key.acc_address,
        RECIPIENT,
        Coins(uluna=1000000, ukrw=1000000)
    )

    # create and sign a transaction
    send_tx = wallet.create_and_sign_tx(
        msgs=[send_msg],
        memo="Hello, Terra!"
    )

    # broadcast the tx and print results
    result = terra.tx.broadcast(send_tx)
    print(result)

