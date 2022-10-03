from terra_sdk.client.lcd import LCDClient


def main():
    terra = LCDClient(
        url="https://phoenix-lcd.terra.dev",
        chain_id="phoenix-1",
    )
    print(terra.tx.tx_infos_by_height(1763383))

main()
