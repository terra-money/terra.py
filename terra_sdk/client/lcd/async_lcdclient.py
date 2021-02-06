from __future__ import annotations

from asyncio import AbstractEventLoop, get_event_loop
from typing import Optional
from urllib.parse import urljoin

from aiohttp import ClientSession

from terra_sdk.core import Coins, Numeric
from terra_sdk.exceptions import LCDResponseError
from terra_sdk.key.key import Key
from terra_sdk.util.json import dict_to_data

from .api.auth import AsyncAuthAPI
from .api.bank import AsyncBankAPI
from .api.distribution import AsyncDistributionAPI
from .api.gov import AsyncGovAPI
from .api.market import AsyncMarketAPI
from .api.mint import AsyncMintAPI
from .api.msgauth import AsyncMsgAuthAPI
from .api.oracle import AsyncOracleAPI
from .api.slashing import AsyncSlashingAPI
from .api.staking import AsyncStakingAPI
from .api.supply import AsyncSupplyAPI
from .api.tendermint import AsyncTendermintAPI
from .api.treasury import AsyncTreasuryAPI
from .api.tx import AsyncTxAPI
from .api.wasm import AsyncWasmAPI
from .wallet import AsyncWallet


class AsyncLCDClient:
    def __init__(
        self,
        url: str,
        chain_id: str = None,
        gas_prices: Coins.Input = None,
        gas_adjustment: Numeric.Input = None,
        loop: Optional[AbstractEventLoop] = None,
    ):

        if loop is None:
            loop = get_event_loop()

        self.session = ClientSession(headers={"Accept": "application/json"}, loop=loop)
        self.chain_id = chain_id
        self.url = url
        self.gas_prices = Coins(gas_prices)
        self.gas_adjustment = gas_adjustment
        self._last_request_height = None

        self.auth = AsyncAuthAPI(self)
        self.bank = AsyncBankAPI(self)
        self.distribution = AsyncDistributionAPI(self)
        self.gov = AsyncGovAPI(self)
        self.market = AsyncMarketAPI(self)
        self.mint = AsyncMintAPI(self)
        self.msgauth = AsyncMsgAuthAPI(self)
        self.oracle = AsyncOracleAPI(self)
        self.slashing = AsyncSlashingAPI(self)
        self.staking = AsyncStakingAPI(self)
        self.supply = AsyncSupplyAPI(self)
        self.tendermint = AsyncTendermintAPI(self)
        self.treasury = AsyncTreasuryAPI(self)
        self.wasm = AsyncWasmAPI(self)
        self.tx = AsyncTxAPI(self)

    def wallet(self, key: Key) -> AsyncWallet:
        return AsyncWallet(self, key)

    async def _get(
        self, endpoint: str, params: Optional[dict] = None, raw: bool = False
    ):
        async with self.session.get(
            urljoin(self.url, endpoint), params=params
        ) as response:
            result = await response.json()
            if not str(response.status).startswith("2"):
                raise LCDResponseError(message=result.get("error"), response=response)
        try:
            self._last_request_height = result["height"]
        except KeyError:
            self._last_request_height = None
        return result if raw else result["result"]

    async def _post(
        self, endpoint: str, data: Optional[dict] = None, raw: bool = False
    ):
        async with self.session.post(
            urljoin(self.url, endpoint), json=data and dict_to_data(data)
        ) as response:
            result = await response.json()
            if not str(response.status).startswith("2"):
                raise LCDResponseError(message=result.get("error"), response=response)
        try:
            self._last_request_height = result["height"]
        except KeyError:
            self._last_request_height = None
        return result if raw else result["result"]

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()
