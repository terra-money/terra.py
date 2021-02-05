from terra_sdk.client.lcd import LCDClient
from terra_sdk.util.runner import run_with_lcdclient


async def main(terra: LCDClient):
    print(await terra.auth.account_info("terra1gqvk49ze9rp4nl9tcu5y70u6ta0g7kxhm8mjgy"))


run_with_lcdclient(main, chain_id="columbus-4", url="https://lcd.terra.dev")
