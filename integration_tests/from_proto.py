from terra_sdk.client.lcd import AsyncLCDClient
from terra_sdk.core import Coins
from terra_sdk.core.authz import MsgExecAuthorized
from terra_sdk.core.bank import MsgMultiSend
from terra_sdk.core.crisis import MsgVerifyInvariant
import requests, asyncio

light_clinet_address = 'https://lcd.terra.dev'
chain_id = 'columbus-5'
gas_prices = requests.get('https://fcd.terra.dev/v1/txs/gas_prices').json()
terra = AsyncLCDClient(chain_id=chain_id,
                       url=light_clinet_address,
                       gas_prices=Coins(uusd=gas_prices['uusd']),
                       gas_adjustment=1.2)


async def main():
    async with terra:
        height = 0
        types = {}
        while True:
            bi = await terra.tendermint.block_info()
            block = bi['block']
            if height != block['header']['height']:
                height = block['header']['height']
                for encoded_tx in block['data']['txs']:
                    try:
                        tx = await terra.tx.decode(encoded_tx)
                        for msg in tx.body.messages:
                            if isinstance(msg, MsgExecAuthorized):
                                print('MsgExecAuthorized.from_proto fixed')
                            elif isinstance(msg, MsgMultiSend):
                                print('MsgMultiSend.unpack_any fixed')
                            elif isinstance(msg, MsgVerifyInvariant):
                                print('MsgVerifyInvariant.unpack_any fixed')
                            else:
                                t = type(msg)
                                if t.__name__ not in types:
                                    types[t.__name__] = t
                                    print(f'{t.__name__}.from_proto/unpack_any checked')
                    except Exception as exc:
                        print(exc)
            await asyncio.sleep(7)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
