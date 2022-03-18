from terra_sdk.client.lcd import LCDClient

terra = LCDClient(chain_id="columbus-5", url="https://lcd.terra.dev")
print(terra.tx.tx_info('da66fac2c941d3862f743ceac2b343ff47348883e894c00506cdc58a202a5b81'))
