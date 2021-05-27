from terra_sdk.client.lcd import LCDClient

bombay = LCDClient(url="https://bombay-lcd.terra.dev", chain_id="bombay-0001")

address = "terra1fa0trn2nqjc2n6mmz9txta7ky5h5nnp9m6cra3"
account_balance = bombay.bank.balance(address)
assert account_balance is not None
