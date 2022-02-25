from terra_sdk.client.lcd import LCDClient, PaginationOptions


def main():
    terra = LCDClient(
        url="https://bombay-lcd.terra.dev/",
        chain_id="bombay-12",
    )

    result = terra.mint.inflation()
    print(result)
    result = terra.mint.annual_provisions()
    print(result)
    result = terra.mint.parameters()
    print(result)


main()
