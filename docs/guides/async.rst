Usage with asyncio
==================

If you want to make asynchronous, non-blocking LCD requests, you can use AsyncLCDClient.
The interface is similar to LCDClient, except the LCDClient API functions must be awaited.

Async Module APIs
-----------------

You should use  inside a coroutine function:

.. code-block:: python
    :emphasize-lines: 5,8

    import asyncio 
    from terra_sdk.client.lcd import AsyncLCDClient

    async def main():
        terra = AsyncLCDClient("https://lcd.terra.dev", "columbus-4")
        total_supply = await terra.supply.total()
        print(total_supply)
        await terra.session.close() # you must close the session

    asyncio.get_event_loop().run_until_complete(main())


Here's the same code, but using the async context manager to teardown the session:

.. code-block:: python
    :emphasize-lines: 5

    import asyncio 
    from terra_sdk.client.lcd import AsyncLCDClient

    async def main():
        async with AsyncLCDClient("https://lcd.terra.dev", "columbus-4") as terra:
            total_supply = await terra.supply.total()
            print(total_supply)

    asyncio.get_event_loop().run_until_complete(main())

Async Wallet API
----------------

When creating a wallet with AsyncLCDClient, the wallet's methods must also be awaited.

.. code-block:: python
    :emphasize-lines: 12-13

    import asyncio 
    from terra_sdk.client.lcd import AsyncLCDClient
    from terra_sdk.key.mnemonic import MnemonicKey
    from terra_sdk.core import Coins

    mk = MnemonicKey()
    recipient = "terra1..."

    async def main():
        async with AsyncLCDClient("https://lcd.terra.dev", "columbus-4") as terra:
            wallet = terra.wallet(mk)
            account_number = await wallet.account_number()
            tx = await wallet.create_and_sign_tx(
                msgs=[MsgSend(wallet.key.acc_address, recipient, Coins(uluna=10202))]
            )
    
    asyncio.get_event_loop().run_until_complete(main())

Alternative Event Loops
-----------------------

You can swap out the native ``asyncio`` event loop for something like ``uvloop`` if you
need:

.. code-block:: python
    :emphasize-lines: 2, 10

    import asyncio
    import uvloop

    from terra_sdk.client.lcd import AsyncLCDClient

    async def main():
        async with AsyncLCDClient("https://lcd.terra.dev", "columbus-4") as terra:
            total_supply = await wallet.supply.total()

    uvloop.install() 
    asyncio.get_event_loop().run_until_complete(main())