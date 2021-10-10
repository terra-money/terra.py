from terra_sdk.client.lcd import LCDClient

terra = LCDClient(chain_id="columbus-5", url="https://silent-restless-snowflake.terra-mainnet.quiknode.pro/166cf94134bb9f132e27d52f456ed967332e8ba3/")
res = terra.tendermint.node_info()
print(res)
terra2 = LCDClient(chain_id="columbus-5", url="https://lcd.terra.dev")
res = terra2.tx.tx_info('42DE8348A333613EB013251DE2056EE301019DA8C2505935B24E8596AFD350A1')
print(res)
