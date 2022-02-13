Keys & Wallets
==============

A **Key** is an object that provides an abstraction for the agency of signing transactions.

Key (abstract)
--------------

Implementers of Keys meant for signing should override :meth:`Key.sign()<terra_sdk.key.Key.sign>`
or :meth:`Key.create_signature()<terra_sdk.key.key.Key.create_signature>` methods. More details are
available in :ref:`guides/custom_key`.

Some properties such as :meth:`acc_address<terra_sdk.key.key.Key.acc_address>` and
:meth:`val_address<terra_sdk.key.key.Key.val_address>` are provided.

.. automodule:: terra_sdk.key.key
    :members:

RawKey
------

.. automodule:: terra_sdk.key.raw
    :members:


MnemonicKey
-----------

.. automodule:: terra_sdk.key.mnemonic
    :members:

Wallet
------

.. automodule:: terra_sdk.client.lcd.wallet
    :members: