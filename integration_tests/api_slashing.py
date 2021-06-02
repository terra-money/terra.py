from terra_sdk.client.lcd import LCDClient

bombay = LCDClient(url="https://bombay-lcd.terra.dev", chain_id="bombay-0001")

parameters = bombay.slashing.parameters()
assert "signed_blocks_window" in parameters
assert "min_signed_per_window" in parameters
assert "downtime_jail_duration" in parameters
assert "slash_fraction_double_sign" in parameters
assert "slash_fraction_downtime" in parameters

signing_infos = bombay.slashing.signing_infos()
assert type(signing_infos[0]) == dict if len(signing_infos) > 0 else True
