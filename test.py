import asyncio
from terra_sdk.client.lcd import LCDClient


async def main():
    async with LCDClient("https://lcd.terra.dev") as terra:
        item = await terra.gov.proposer(2)
        print(item)


loop = asyncio.new_event_loop()
loop.run_until_complete(main())