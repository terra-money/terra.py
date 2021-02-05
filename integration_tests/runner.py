import asyncio

from terra_sdk.client.lcd import LCDClient
from terra_sdk.util.runner import run_with_lcdclient


async def main(terra: LCDClient):
    print(await terra.supply.total())


run_with_lcdclient(main, chain_id="columbus-4", url="https://lcd.terra.dev")
