from terra_sdk.client.lcd import LCDClient

terra = LCDClient(chain_id="pisco-1", url="https://pisco-lcd.terra.dev")
print(
    terra.distribution.validator_rewards(
        "terravaloper1259cmu5zyklsdkmgstxhwqpe0utfe5hhyty0at"
    )
)
