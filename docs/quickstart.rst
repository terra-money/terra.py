.. _quickstart:

Quickstart
==========

.. contents:: :local:

.. NOTE:: All code starting with a ``$`` is meant to run on your terminal.
    All code starting with a ``>>>`` is meant to run in a python interpreter,
    like `ipython <https://pypi.org/project/ipython/>`_.

Installation
------------

Terra SDK can be installed (preferably in a :ref:`virtualenv <setup_environment>`)
using ``pip`` as follows:

.. code-block:: shell

   $ pip install terra_sdk 


.. NOTE:: If you run into problems during installation, you might have a
    broken environment. See the troubleshooting guide to :ref:`setting up a
    clean environment <setup_environment>`.


Using Terra SDK
---------------

In order to interact with the Terra blockchain, you'll need a connection to a Terra node.
This can be done through setting up an LCDClient:


.. code-block:: python

    from terra_sdk.client.lcd import LCDClient

    terra = LCDClient(chain_id="columbus-4", url="https://lcd.terra.dev")
    print(terra.tendermint.node_info())


Getting Blockchain Info
-----------------------

It's time to start using Terra SDK! Once properly configured, the ``LCDClient`` instance will allow you
to interact with the Terra blockchain. Try getting the latest block height:

.. code-block:: python

    >>> terra.tendermint.block_info()['block']['header']['height']
    '1687543'

Terra SDK can help you read block data, sign and send transactions, deploy and interact with contracts,
and a number of other features.

Many of the typical things you'll want to do will be in the :class:`terra_sdk.client.lcd.LCDClient <web3.eth.Eth>` API,
so that is a good place to start.

If you want to dive straight into contracts, check out the section on :ref:`contracts`,
including a :ref:`contract_example`, and how to create a contract instance using
:class:`terra_sdk.core.MsgStoreCode <web3.eth.Eth.contract>`.

.. NOTE:: It is recommended that your development environment have the ``PYTHONWARNINGS=default``
    environment variable set. Some deprecation warnings will not show up
    without this variable being set.