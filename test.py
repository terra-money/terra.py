import asyncio
from terra_sdk.client.lcd import LCDClient
from terra_sdk.core.coin import Coin


async def main():
    async with LCDClient("https://lcd.terra.dev") as terra:
        item = await terra.wasm.parameters()
        print(item)


loop = asyncio.new_event_loop()
loop.run_until_complete(main())