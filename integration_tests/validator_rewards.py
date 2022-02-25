from terra_sdk.client.lcd import LCDClient

terra = LCDClient(chain_id="bombay-12", url="https://bombay-lcd.terra.dev")
print(terra.distribution.validator_rewards("terravaloper1259cmu5zyklsdkmgstxhwqpe0utfe5hhyty0at"))

