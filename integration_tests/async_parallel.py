import asyncio
from terra_sdk.client.lcd import AsyncLCDClient


async def hello():
    terra = AsyncLCDClient(url="https://lcd.terra.dev", chain_id="columbus-4")

    result = await asyncio.gather(
        terra.oracle.misses("terravaloper1krj7amhhagjnyg2tkkuh6l0550y733jnjnnlzy"),
        terra.oracle.misses("terravaloper1krj7amhhagjnyg2tkkuh6l0550y733jnjnnlzy"),
    )

    await terra.session.close()

    return result


asyncio.get_event_loop().run_until_complete(hello())