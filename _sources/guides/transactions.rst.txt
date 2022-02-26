Building and Signing Transactions
=================================

If you want to perform a state-changing operation on the Terra blockchain such as
sending tokens, swapping assets, withdrawing rewards, or even invoking functions on
smart contracts, you must create a **transaction** and broadcast it to the network.

An :class:`StdTx<terra_sdk.core.tx.Tx>` is a data object that represents
a transaction. It contains:

- **msgs**: a list of state-altering messages
- **fee**: the transaction fee paid to network / validators
- **signatures**: a list of signatures from required signers (depends on messages)
- **memo**: a short string describing transaction (can be empty string)

Terra SDK provides functions that help create StdTx objects.

Using a Wallet (recommended)
----------------------------

.. note::
    This method requires an LCDClient instance with a proper node connection. If you
    can't use Wallet, see `Signing transactions manually`_.

A :class:`Wallet<terra_sdk.client.lcd.wallet.Wallet>` allows you to create and sign a transaction in a single step by automatically
fetching the latest information from the blockchain (chain ID, account number, sequence).

Use :meth:`LCDClient.wallet()<terra_sdk.client.lcd.LCDClient.wallet>` to create a Wallet from any Key instance. The Key provided should
correspond to the account you intend to sign the transaction with.

.. code-block:: python

    from terra_sdk.client.lcd import LCDClient
    from terra_sdk.key.mnemonic import MnemonicKey

    mk = MnemonicKey(mnemonic=MNEMONIC) 
    terra = LCDClient("https://lcd.terra.dev", "columbus-5")
    wallet = terra.wallet(mk)


Once you have your Wallet, you can simply create a StdTx using :meth:`Wallet.create_and_sign_tx`.

.. code-block:: python

    from terra_sdk.client.lcd.api.tx import CreateTxOptions
    from terra_sdk.core.fee import Fee
    from terra_sdk.core.bank import MsgSend

    tx = wallet.create_and_sign_tx(
        CreateTxOptions(
            msgs=[MsgSend(
                wallet.key.acc_address,
                RECIPIENT,
                "1000000uluna" # send 1 luna
            )]
            ,
            memo="test transaction!",
            fee=Fee(200000, "120000uluna")
        )
    )

And that's it! You should now be able to broadcast your transaction to the network.

.. code-block:: python

    result = terra.tx.broadcast(tx)
    print(result)

Automatic fee estimation
^^^^^^^^^^^^^^^^^^^^^^^^

If no ``fee`` parameter is provided for :meth:`Wallet.create_and_sign_tx()<terra_sdk.client.lcd.wallet.Wallet.create_and_sign_tx>`,
the transaction fee will be simulated against the node and populated for you. By default, ``Wallet``
will use the fee estimation parameters of the ``LCDClient`` used to create it. You can override
this behavior **per transaction**:

.. important::
    Fee estimation simulates the transaction in the node -- if the transaction would fail
    due to an error, such as an incorrect smart contract call, the estimation too would fail.

.. note::
    By default, the estimated fee returned consists of a fee paid in every denom for which the
    signing account hold a balance. For instance, if the signer has a balance of ``uusd`` and ``uluna``,
    the fee reported will be both ``uusd`` and ``uluna``. 
    
    Use the ``denoms`` argument to restrict the estimated fee to specific denoms.


.. code-block:: python
    :emphasize-lines: 8-10

    tx = wallet.create_and_sign_tx(CreateTxOptions(
        msgs=[MsgSend(
            wallet.key.acc_address,
            RECIPIENT,
            "1000000uluna" # send 1 luna
        )],
        memo="test transaction!",
        gas_prices="0.015uluna,0.11ukrw", # optional
        gas_adjustment="1.2", # optional
        denoms=["ukrw"] # optional
    ))

Signing transactions manually
-----------------------------

Below is the full process of signing a transaction manually that does not use ``Wallet``.
You will need to build a :class:`SignDoc<terra_sdk.core.sign_doc.SignDoc>`,
sign it, and add the signatures to an ``Tx``.

A SignDoc contains the information required to build a StdTx:

- **chain_id**: chain ID of blockchain network
- **account_number**: account number in blockchain
- **sequence**: sequence number (# of prior transactions)
- **auth_info**: transaction authentication info
- **tx_body**: body of a transaction. containing messages.

.. code-block:: python

    from terra_sdk.client.lcd.api.tx import CreateTxOptions, SignerOptions
    from terra_sdk.client.lcd import LCDClient
    from terra_sdk.core.bank import MsgSend
    from terra_sdk.core.tx import SignMode
    from terra_sdk.key.key import SignOptions
    from terra_sdk.key.mnemonic import MnemonicKey
    from terra_sdk.core import Coin, Coins

    terra = LCDClient("https://lcd.terra.dev", "columbus-5")
    key = MnemonicKey(mnemonic=MNEMONIC)

    msg = MsgSend(
        key.acc_address,
        "terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v",
        Coins(uluna=30000),
    )

    tx_opt = CreateTxOptions(
        msgs=[msg], memo="send test", gas_adjustment=1.5
    )

    signer_opt = SignerOptions(
        address=key.acc_address,
    )

    acc_info = terra.auth.account_info(key.acc_address)

    sign_opt = SignOptions(
        account_number=acc_info.account_number,
        sequence=acc_info.sequence,
        sign_mode=SignMode.SIGN_MODE_DIRECT,
        chain_id='columbus-5'
    )

    tx = terra.tx.create([signer_opt], tx_opt)

    signed_tx = key.sign_tx(tx, sign_opt)

    # broadcast tx
    result = terra.tx.broadcast(signed_tx)
    print(result)



Applying multiple signatures
----------------------------

Some messages, such as ``MsgMultiSend``, require the transaction to be signed with multiple signatures.
You must prepare a separate ``SignDoc`` for each signer to sign individually, and then
combine them in the ``signatures`` field of the final :class:`StdTx<terra_sdk.core..tx.Tx>` object. 
Each ``SignDoc`` should only differ by ``account`` and ``sequence``, which vary according to the signing key.

.. note::
    In a transaction with multiple signers, the account of the first signature in the
    ``StdTx`` is responsible for paying the fee.

.. code-block:: python

    from terra_sdk.client.lcd import LCDClient
    from terra_sdk.core.fee import Fee
    from terra_sdk.core.bank import MsgMultiSend
    from terra_sdk.key.mnemonic import MnemonicKey
    from terra_sdk.core.bank import MsgMultiSend, MultiSendInput, MultiSendOutput

    terra = LCDClient("https://lcd.terra.dev", "columbus-5")
    wallet1 = terra.wallet(MnemonicKey(mnemonic=MNEMONIC_1))
    wallet2 = terra.wallet(MnemonicKey(mnemonic=MNEMONIC_2))

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
            address=wallet1.key.acc_address,
            coins=Coins(uluna=20000),
        ),
        MultiSendOutput(
            address=wallet2.key.acc_address,
            coins=Coins(uluna=10000),
        ),
    ]

    msg = MsgMultiSend(inputs, outputs)

    opt = CreateTxOptions(
        msgs=[msg]
    )

    tx = terra.tx.create(
        [SignerOptions(address=wallet1.key.acc_address), SignerOptions(address=wallet2.key.acc_address)], opt)

    info1 = wallet1.account_number_and_sequence()
    info2 = wallet2.account_number_and_sequence()

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

    result = terra.tx.broadcast(tx)
    print(result)


Signing multiple offline transactions
-------------------------------------

In some cases, you may wish to sign and save multiple transactions in
advance, in order to broadcast them at a later date. To do so, you will
need to manually update the **sequence** number to override the ``Wallet``'s
automatic default behavior of loading the latest sequence number from the
blockchain (which will not have been updated).

.. code-block:: python
    :emphasize-lines: 2,5,10,15

    # get first sequence
    sequence = wallet.sequence()
    tx1 = wallet.create_and_sign_tx(
        CreateTxOptions(
            msgs=[MsgSend(...)],
            sequence=sequence
        )
    )

    tx2 = wallet.create_and_sign_tx(
        CreateTxOptions(
            msgs=[MsgSwap(...)],
            sequence=sequence+1
        )
    )

    tx3 = wallet.create_and_sign_tx(
        CreateTxOptions(
            msgs=[MsgExecuteContract(...)],
            sequence=sequence+2
        )
    )


