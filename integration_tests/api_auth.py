from terra_sdk.client.lcd import LCDClient

bombay = LCDClient(url="https://bombay-lcd.terra.dev", chain_id="bombay-0001")

base_account_address = "terra1fa0trn2nqjc2n6mmz9txta7ky5h5nnp9m6cra3"
base_account_data = {
    "type": "core/Account",
    "value": {
      "address": "terra1fa0trn2nqjc2n6mmz9txta7ky5h5nnp9m6cra3",
      "public_key": {
        "type": "tendermint/PubKeySecp256k1",
        "value": "A6/5zM6Vo11e3aepClYLVn4rsHdXOnFsDccXYiuvSeeJ"
      },
      "account_number": "27",
      "sequence": "0"
    }
}
base_account = bombay.auth.account_info(base_account_address)
base_account.sequence = 0  # Set sequence # to 0 since it's dynamic
assert base_account.to_data() == base_account_data
