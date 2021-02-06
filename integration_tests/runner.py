from terra_sdk.client.lcd import AsyncLCDClient
from terra_sdk.util.runner import run_with_async_client


async def main(terra: AsyncLCDClient):
    print(await terra.auth.account_info("terra1gqvk49ze9rp4nl9tcu5y70u6ta0g7kxhm8mjgy"))


run_with_async_client(main, chain_id="columbus-4", url="https://lcd.terra.dev")
