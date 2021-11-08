from terra_sdk.client.lcd import LCDClient

terra = LCDClient(chain_id="bombay-12", url="https://bombay-lcd.terra.dev")

res = terra.auth.account_info(address="terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v")
print(res)

res = terra.auth.account_info(address="terra1vk20anceu6h9s00d27pjlvslz3avetkvnph7p8")
print(res)
