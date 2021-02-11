.. keys:

Guide to using Keys
===================

Key Types
---------

RawKey
^^^^^^

.. autoclass:: terra_sdk.key.raw.RawKey
    :members:


MnemonicKey
^^^^^^^^^^^

.. autoclass:: terra_sdk.key.mnemonic.MnemonicKey
    :members:

.. code-block:: python

    >>> from terra_sdk.key.mnemonic import MnemonicKey

    >>> mk = MnemonicKey()
    >>> mk.mnemonic

Writing Your Own Key
--------------------

Key
^^^

.. autoclass:: terra_sdk.key.key.Key
    :members:

Usage with Wallet
-----------------

