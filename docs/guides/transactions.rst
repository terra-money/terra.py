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
    terra = LCDClient("https://lcd.terra.dev", "columbus-4")
    wallet = terra.wallet(mk)


Once you have your Wallet, you can simply create a StdTx using :meth:`Wallet.create_and_sign_tx`.

.. code-block:: python

    from terra_sdk.core.fee import Fee
    from terra_sdk.core.bank import MsgSend

    tx = wallet.create_and_sign_tx(
        msgs=[MsgSend(
            wallet.key.acc_address,
            RECIPIENT,
            "1000000uluna" # send 1 luna
        )],
        memo="test transaction!",
        fee=Fee(200000, "120000uluna")
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

    tx = wallet.create_and_sign_tx(
        msgs=[MsgSend(
            wallet.key.acc_address,
            RECIPIENT,
            "1000000uluna" # send 1 luna
        )],
        memo="test transaction!",
        gas_prices="0.015uluna,0.11ukrw", # optional
        gas_adjustment="1.2", # optional
        denoms=["ukrw"] # optional
    )

Signing transactions manually
-----------------------------

Below is the full process of signing a transaction manually that does not use ``Wallet``.
You will need to build a :class:`StdSignMsg<terra_sdk.core..tx.SignDoc>`, 
sign it, and add the signatures to an ``StdTx``.

A StdSignMsg contains the information required to build a StdTx:

- **chain_id**: chain ID of blockchain network
- **account_number**: account number in blockchain
- **sequence**: sequence number (# of prior transactions)
- **fee**: the transaction fee paid to network / validators
- **msgs**: list of messages to include
- **memo**: a short string describing transaction (can be empty string)

.. code-block:: python

    from terra_sdk.client.lcd import LCDClient
    from terra_sdk.core.auth import StdSignMsg
    from terra_sdk.core.bank import MsgSend
    from terra_sdk.key.mnemonic import MnemonicKey

    terra = LCDClient("https://lcd.terra.dev", "columbus-4")
    mk = MnemonicKey(mnemonic=MNEMONIC) 

    # create tx
    unsigned_tx = StdSignMsg(
        chain_id="columbus-4",
        account_number=23982,
        sequence=12,
        fee=Fee(200000, "120000uluna"),
        msgs=[MsgSend(
            mk.acc_address,
            RECIPIENT,
            "1000000uluna" # send 1 luna
        )],
        memo="test transaction!"
    )

    # get signature
    sig = mk.create_signature(unsigned_tx)

    # prepopulate stdtx with details
    tx = unsigned_tx.to_stdtx()

    # apply signature
    tx.signature = [sig]

    # broadcast tx
    result = terra.tx.broadcast(tx)
    print(result)



Applying multiple signatures
----------------------------

Some messages, such as ``MsgMultiSend``, require the transaction to be signed with multiple signatures.
You must prepare a separate ``StdSignMsg`` for each signer to sign individually, and then
combine them in the ``signatures`` field of the final :class:`StdTx<terra_sdk.core..tx.Tx>` object. 
Each ``StdSignMsg`` should only differ by ``account`` and ``sequence``, which vary according to the signing key.

.. note::
    In a transaction with multiple signers, the account of the first signature in the
    ``StdTx`` is responsible for paying the fee.

.. code-block:: python

    from terra_sdk.client.lcd import LCDClient
    from terra_sdk.core.fee import Fee
    from terra_sdk.core.bank import MsgMultiSend
    from terra_sdk.key.mnemonic import MnemonicKey

    terra = LCDClient("https://lcd.terra.dev", "columbus-4")
    wallet1 = terra.wallet(MnemonicKey(mnemonic=MNEMONIC_1))
    wallet2 = terra.wallet(MnemonicKey(mnemonic=MNEMONIC_2))

    multisend = MsgMultiSend(
        inputs=[
            {"address": wallet1.key.acc_address, "coins": "12000uusd,11000uluna"},
            {"address": wallet2.key.acc_address, "coins": "11000ukrw,10000uluna"}
        ],
        outputs=[
            {"address": wallet1.key.acc_address, "coins": "11000ukrw,10000uluna"},
            {"address": wallet2.key.acc_address, "coins": "12000uusd,11000uluna"}
        ]    
    )

    msgs = [multisend]
    fee = Fee(200000, "12000uluna")
    memo = "multisend example"

    # create unsigned_tx #1
    u_tx1 = wallet1.create_tx(
        msgs=msgs,
        fee=fee,
        memo=memo
    )

    sig1 = wallet1.key.create_signature(u_tx1)

    # create unsigned tx #2
    u_tx2 = wallet2.create_tx(
        msgs=msgs,
        fee=fee,
        memo=memo
    )

    sig2 = wallet2.key.create_signature(u_tx2)

    # build stdtx
    tx = u_tx1.to_stdtx()

    # apply signatures
    tx.signatures = [sig1, sig2]

    # broadcast tx
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
        msgs=[MsgSend(...)],
        sequence=sequence
    )

    tx2 = wallet.create_and_sign_tx(
        msgs=[MsgSwap(...)],
        sequence=sequence+1
    )

    tx3 = wallet.create_and_sign_tx(
        msgs=[MsgExecuteContract(...)],
        sequence=sequence+2
    )


