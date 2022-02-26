LCDClient
=========

The :class:`LCDClient` is an object representing a HTTP connection to a Terra LCD node.

Get connected
-------------

Create a new LCDClient instance by specifying the URL and chain ID of the node to connect to.

.. note::
    It is common practice to name the active LCDClient instance ``terra``, but this is not required.

.. code-block:: python

    >>> from terra_sdk.client.lcd import LCDClient
    >>> terra = LCDClient(url="https://lcd.terra.dev", chain_id="columbus-5")
    >>> terra.tendermint.node_info()['default_node_info']['network']
    'columbus-5'

You can also specify gas estimation parameters for your chain for building transactions.

.. code-block:: python
    :emphasize-lines: 8-9

    import requests
    from terra_sdk.core import Coins

    res = requests.get("https://fcd.terra.dev/v1/txs/gas_prices")
    terra = LCDClient(
        url="https://lcd.terra.dev",
        chain_id="columbus-5",
        gas_prices=Coins(res.json()),
        gas_adjustment="1.4"
    )    


Using the module APIs
---------------------

LCDClient includes functions for interacting with each of the core modules (see sidebar). These functions are divided and
and organized by module name (eg. :class:`terra.market<terra_sdk.client.lcd.api.market.MarketAPI>`), and handle 
the tedium of building HTTP requests, parsing the results, and handling errors. 

Each request fetches live data from the blockchain:

.. code-block:: python

    >>> terra.market.parameters()
    {'base_pool': '7000000000000.000000000000000000', 'pool_recovery_period': '200', 'min_spread': '0.005000000000000000'}

The height of the last result (if applicable) is available:

.. code-block:: python

    >>> terra.last_request_height
    89292


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
