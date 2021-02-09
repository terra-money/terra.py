from __future__ import annotations

from asyncio import AbstractEventLoop, get_event_loop
from typing import Optional
from urllib.parse import urljoin

import nest_asyncio
from aiohttp import ClientSession

from terra_sdk.core import Coins, Numeric
from terra_sdk.exceptions import LCDResponseError
from terra_sdk.key.key import Key
from terra_sdk.util.json import dict_to_data

from .api.auth import AsyncAuthAPI, AuthAPI
from .api.bank import AsyncBankAPI, BankAPI
from .api.distribution import AsyncDistributionAPI, DistributionAPI
from .api.gov import AsyncGovAPI, GovAPI
from .api.market import AsyncMarketAPI, MarketAPI
from .api.mint import AsyncMintAPI, MintAPI
from .api.msgauth import AsyncMsgAuthAPI, MsgAuthAPI
from .api.oracle import AsyncOracleAPI, OracleAPI
from .api.slashing import AsyncSlashingAPI, SlashingAPI
from .api.staking import AsyncStakingAPI, StakingAPI
from .api.supply import AsyncSupplyAPI, SupplyAPI
from .api.tendermint import AsyncTendermintAPI, TendermintAPI
from .api.treasury import AsyncTreasuryAPI, TreasuryAPI
from .api.tx import AsyncTxAPI, TxAPI
from .api.wasm import AsyncWasmAPI, WasmAPI
from .wallet import AsyncWallet, Wallet


class AsyncLCDClient:
    def __init__(
        self,
        url: str,
        chain_id: str = None,
        gas_prices: Coins.Input = None,
        gas_adjustment: Numeric.Input = None,
        loop: Optional[AbstractEventLoop] = None,
        _create_session: bool = True,  # don't create a session (used for sync LCDClient)
    ):
        if loop is None:
            loop = get_event_loop()
        self.loop = loop
        if _create_session:
            self.session = ClientSession(
                headers={"Accept": "application/json"}, loop=self.loop
            )

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


class LCDClient(AsyncLCDClient):
    def __init__(self, *args, **kwargs):
        options = {
            **kwargs,
            "_create_session": False,
            "loop": nest_asyncio.apply(get_event_loop()),
        }
        super().__init__(*args, **options)

        self.auth = AuthAPI(self)
        self.bank = BankAPI(self)
        self.distribution = DistributionAPI(self)
        self.gov = GovAPI(self)
        self.market = MarketAPI(self)
        self.mint = MintAPI(self)
        self.msgauth = MsgAuthAPI(self)
        self.oracle = OracleAPI(self)
        self.slashing = SlashingAPI(self)
        self.staking = StakingAPI(self)
        self.supply = SupplyAPI(self)
        self.tendermint = TendermintAPI(self)
        self.treasury = TreasuryAPI(self)
        self.wasm = WasmAPI(self)
        self.tx = TxAPI(self)

    async def __aenter__(self):
        raise NotImplementedError(
            "async context manager not implemented - you probably want AsyncLCDClient"
        )

    async def __aexit__(self, exc_type, exc, tb):
        raise NotImplementedError(
            "async context manager not implemented - you probably want AsyncLCDClient"
        )

    def wallet(self, key: Key) -> Wallet:  # type: ignore
        return Wallet(self, key)

    async def _get(self, *args, **kwargs):
        # session has to be manually created and torn down for each HTTP request in a
        # synchronous client
        self.session = ClientSession(
            headers={"Accept": "application/json"}, loop=self.loop
        )
        try:
            result = await super()._get(*args, **kwargs)
        finally:
            await self.session.close()
        return result

    async def _post(self, *args, **kwargs):
        # session has to be manually created and torn down for each HTTP request in a
        # synchronous client
        self.session = ClientSession(
            headers={"Accept": "application/json"}, loop=self.loop
        )
        try:
            result = await super()._post(*args, **kwargs)
        finally:
            await self.session.close()
        return result
