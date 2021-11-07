from terra_sdk.client.lcd import LCDClient, PaginationOptions


def main():
    terra = LCDClient(
        url="https://bombay-lcd.terra.dev/",
        chain_id="bombay-12",
    )

    result = terra.auth.account_info("terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v")
    print(result)


main()
