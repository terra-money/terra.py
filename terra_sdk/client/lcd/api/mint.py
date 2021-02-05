from terra_sdk.core import Dec

from ._base import BaseAPI


class MintAPI(BaseAPI):
    async def inflation(self) -> Dec:
        return Dec(await self._c._get("/minting/inflation"))

    async def annual_provisions(self) -> Dec:
        return Dec(await self._c._get("/minting/annual-provisions"))

    async def parameters(self) -> dict:
        return await self._c._get("/minting/parameters")
