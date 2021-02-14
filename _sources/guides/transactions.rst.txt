Building and Signing Transactions
=================================

If you want to perform a state-changing operation on the Terra blockchain such as
sending tokens, swapping assets, withdrawing rewards, or even invoking functions on
smart contracts, you must create a **transaction** and broadcast it to the network.

The data object repesenting a transaction is :class:`StdTx`. It contains:

- **msgs**: a list of state-altering messages
- **fee**: the transaction fee paid to network / validators
- **signatures**: a list of signatures from required signers (depends on messages)
- **memo**: a short string describing transaction (can be empty string)

Terra SDK provides tools that greatly simplify the process of generating a StdTx object.

Using a Wallet (recommended)
----------------------------

.. note:: This method requires an LCDClient instance with a proper node connection.

.. note::
    Some transactions containing messages like :class:`MsgMultiSend` that require 
    multiple signers cannot be signed using Wallet. See `Signing transactions manually`_.

A :class:`Wallet` allows you to create and sign a transaction in a single step by automatically
fetching the latest information from the blockchain (chain ID, account number, sequence).

Use :meth:`LCDClient.wallet` to create a Wallet from any Key instance. The Key provided should
correspond to the account you intend to sign the transaction with.

.. code-block:: python

    from terra_sdk.client.lcd import LCDClient
    from terra_sdk.key.mnemonic import MnemonicKey

    mk = MnemonicKey(mnemonic=MNEMONIC) 
    terra = LCDClient("https://lcd.terra.dev", "columbus-4")
    wallet = terra.wallet(mk)


Once you have your Wallet, you can simply create a StdTx using :meth:`Wallet.create_and_sign_tx`.

.. code-block:: python

    from terra_sdk.core.auth import StdFee
    from terra_sdk.core.bank import MsgSend

    tx = wallet.create_and_sign_tx(
        msgs=[MsgSend(
            wallet.key.acc_address,
            RECIPIENT,
            "1000000uluna" # send 1 luna
        )],
        memo="test transaction!",
        fee=StdFee(200000, "120000uluna")
    )

And that's it! You should now be able to broadcast your transaction to the network.

.. code-block:: python

    result = terra.tx.broadcast(tx)
    print(result)

Fee estimation
^^^^^^^^^^^^^^

If no ``fee`` parameter is provided for :meth:`Wallet.create_and_sign_tx()`, the transaction
fee will be simulated against the node and populated for you. By default, ``Wallet`` will use
the fee estimation parameters of the :class:`LCDClient` used to create it. You can override
this behavior **per transaction**:

.. note::
    The fee simulation by default will return with a fee amount in every denom available 
    for which the signing account's has a Coin balance (it will fail if account has no
    balance). Use the ``denoms`` parameter to restrict estimated fee to only denoms specified.

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

Applying multiple signatures
----------------------------

If you have message that requires multiple signatures, you need to use sign several
different :class:`StdSignMsg` objects individually and then combine them in the ``signatures``
list within the final :class:`StdTx` object.

.. code-block:: python

    from terra_sdk.client.lcd import LCDClient
    from terra_sdk.core.auth import StdFee
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
    fee = StdFee(200000, "12000uluna")
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

Signing transactions manually
-----------------------------

If you prefer not to use ``LCDClient`` or ``Wallet`` for a reason (such as not wanting /
having access to a node, internet, etc.) -- you can sign transactions manually by first
building a :class:`StdSignMsg`.

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
        fee=StdFee(200000, "120000uluna"),
        msgs=[MsgSend(
            mk.acc_address,
            RECIPIENT,
            "1000000uluna" # send 1 luna
        )],
        memo="test transaction!"
    )

    # get signature
    sig = mk.create_signature(unsigned_tx)

    # build stdtx
    tx = unsigned_tx.to_stdtx()

    # apply signature
    tx.signature = [sig]

    # broadcast tx
    result = terra.tx.broadcast(tx)
    print(result)
