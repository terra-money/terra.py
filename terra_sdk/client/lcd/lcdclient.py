from __future__ import annotations

from asyncio import AbstractEventLoop, get_event_loop
from typing import Optional
from urllib.parse import urljoin

from aiohttp import ClientSession

from terra_sdk.core import Coins, Numeric
from terra_sdk.key.key import Key
from terra_sdk.util.json import dict_to_data

from .api.auth import AuthAPI
from .api.bank import BankAPI
from .api.distribution import DistributionAPI
from .api.gov import GovAPI
from .api.market import MarketAPI
from .api.mint import MintAPI
from .api.msgauth import MsgAuthAPI
from .api.oracle import OracleAPI
from .api.slashing import SlashingAPI
from .api.staking import StakingAPI
from .api.supply import SupplyAPI
from .api.tendermint import TendermintAPI
from .api.treasury import TreasuryAPI
from .api.tx import TxAPI
from .api.wasm import WasmAPI
from .wallet import Wallet


class LCDClient:
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

    def wallet(self, key: Key) -> Wallet:
        return Wallet(self, key)

    async def _get(
        self, endpoint: str, params: Optional[dict] = None, raw: bool = False
    ):
        async with self.session.get(
            urljoin(self.url, endpoint), params=params
        ) as response:
            result = await response.json()
        try:
            self._last_request_height = result["height"]
        except KeyError:
            self._last_request_height = None
        print(result)
        return result if raw else result["result"]

    async def _post(
        self, endpoint: str, data: Optional[dict] = None, raw: bool = False
    ):
        async with self.session.post(
            urljoin(self.url, endpoint), json=data and dict_to_data(data)
        ) as response:
            result = await response.json()
        try:
            self._last_request_height = result["height"]
        except KeyError:
            self._last_request_height = None
        return result if raw else result["result"]

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()
