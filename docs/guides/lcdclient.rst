Using LCDClient
===============

The :class:`LCDClient` is an object representing a HTTP connection to a Terra LCD node.

Get connected
-------------

Create a new LCDClient instance by specifying the URL and chain ID of the node to connect to.

.. code-block:: python

    >>> from terra_sdk.client.lcd import LCDClient
    >>> terra = LCDClient("https://lcd.terra.dev", "columbus-4")
    >>> terra.tendermint.node_info()['node_info']['network']
    'columbus-4'

Querying the blockchain
-----------------------

LCDClient includes query functions for each of the core modules (see sidebar). These build and
handle the creation of requests and allow you to easily fetch live data from the blockchain.


.. code-block:: python

    >>> terra.market.parameters()
    {'base_pool': '7000000000000.000000000000000000', 'pool_recovery_period': '200', 'min_spread': '0.005000000000000000'}

Create a wallet
---------------

LCDClient can create a :class:`Wallet` object from any :class:`Key` implementation. Wallet objects
are useful for easily creating and signing transactions.

.. code-block:: python

    >>> from terra_sdk.key.mnemonic import MnemonicKey
    >>> mk = MnemonicKey()
    >>> wallet = terra.wallet(mk)
    >>> wallet.account_number()
    27


LCDClient Reference
-------------------

.. autoclass:: terra_sdk.client.lcd.LCDClient
    :members:

