from terra_sdk.client.lcd import LCDClient


def main():
    terra = LCDClient(
        url="https://bombay-lcd.terra.dev",
        chain_id="bombay-12",
    )

    print(terra.tx.tx_infos_by_height(8152638))
    print(terra.tx.tx_infos_by_height(8153558))


main()
