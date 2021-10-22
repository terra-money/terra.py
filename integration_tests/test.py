import asyncio
import base64
from pathlib import Path

from terra_sdk.client.lcd import LCDClient
from terra_sdk.core import Coins, Coin
from terra_sdk.core.auth import StdFee
from terra_sdk.core.bank import MsgSend
from terra_sdk.util.contract import get_code_id


def main():
    terra = LCDClient(
        url="https://bombay-lcd.terra.dev/",
        chain_id="bombay-12",
    )

    #result = terra.authz.grants('terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v', 'terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp')

    #result = terra.distribution.rewards('terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v')
    #result = terra.distribution.validator_commission('terravaloper19ne0aqltndwxl0n32zyuglp2z8mm3nu0gxpfaw')
    #result = terra.distribution.withdraw_address('terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v')
    #result = terra.distribution.community_pool()
    #result = terra.distribution.parameters()

    #result = terra.gov.proposals()
    #result = terra.gov.proposal(1)      # not working.. tx.height
    #result = terra.gov.deposits(1)       # tx.height problem
    #result = terra.gov.tally(1)
    #result = terra.gov.deposit_parameters()
    #result = terra.gov.voting_parameters()
    #result = terra.gov.tally_parameters()
    #result = terra.gov.parameters()

    #result = terra.market.swap_rate(Coin.parse('10000uluna'), 'uusd')
    #result = terra.market.terra_pool_delta()
    #result = terra.market.parameters()

    #result = terra.mint.inflation()
    #result = terra.mint.annual_provisions()
    #result = terra.mint.parameters()

    #result = terra.oracle.exchange_rates()
    #result = terra.oracle.exchange_rate('ukrw')
    #result = terra.oracle.active_denoms()
    #result = terra.oracle.feeder_address('terravaloper19ne0aqltndwxl0n32zyuglp2z8mm3nu0gxpfaw')
    #result = terra.oracle.misses('terravaloper19ne0aqltndwxl0n32zyuglp2z8mm3nu0gxpfaw')
    #result = terra.oracle.aggregate_prevote('terravaloper19ne0aqltndwxl0n32zyuglp2z8mm3nu0gxpfaw')
    #result = terra.oracle.aggregate_vote('terravaloper19ne0aqltndwxl0n32zyuglp2z8mm3nu0gxpfaw')
    #result = terra.oracle.parameters()

    #result = terra.slashing.signing_infos()
    #result = terra.slashing.signing_info('terravalcons1px544qs6a6m5jxfx5sjtx22mq79chsqxyszhe0')
    #result = terra.slashing.parameters()

    #result = terra.wasm.code_info(3)
    #result = terra.wasm.contract_info('terra1cz7j9y80de9e4lsec5qgw9hdy5lh4r45mvdx98')
    #result = terra.wasm.contract_query('terra1cz7j9y80de9e4lsec5qgw9hdy5lh4r45mvdx98', {"all_allowances":{"owner":"terra1zjwrdt4rm69d84m9s9hqsrfuchnaazhxf2ywpc"}})
    result = terra.wasm.parameters()

    # staking
    # supply
    # tendermint
    # treasury
    # tx

    # ibc
    # ibc-transfer

    print(result)


main()
