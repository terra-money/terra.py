from __future__ import annotations

from asyncio import AbstractEventLoop, get_event_loop
from typing import Optional, Union
from urllib.parse import urljoin

import nest_asyncio
from aiohttp import ClientSession

from terra_sdk.core import Coins, Dec, Numeric
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
        chain_id: Optional[str] = None,
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
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
        self.last_request_height = None

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
        """Creates a :class:`AsyncWallet` object from a key.

        Args:
            key (Key): key implementation
        """
        return AsyncWallet(self, key)

    async def _get(
        self, endpoint: str, params: Optional[dict] = None, raw: bool = False
    ):
        async with self.session.get(
            urljoin(self.url, endpoint), params=params
        ) as response:
            result = await response.json(content_type=None)
            if not str(response.status).startswith("2"):
                raise LCDResponseError(message=result.get("error"), response=response)
        try:
            self.last_request_height = result["height"]
        except KeyError:
            self.last_request_height = None
        return result if raw else result["result"]

    async def _post(
        self, endpoint: str, data: Optional[dict] = None, raw: bool = False
    ):
        async with self.session.post(
            urljoin(self.url, endpoint), json=data and dict_to_data(data)
        ) as response:
            result = await response.json(content_type=None)
            if not str(response.status).startswith("2"):
                raise LCDResponseError(message=result.get("error"), response=response)
        try:
            self.last_request_height = result["height"]
        except KeyError:
            self.last_request_height = None
        return result if raw else result["result"]

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()


class LCDClient(AsyncLCDClient):
    """An object representing a connection to a node running the Terra LCD server."""

    url: str
    """URL endpoint of LCD server."""

    chain_id: str
    """Chain ID of blockchain network connecting to."""

    gas_prices: Coins
    """Gas prices to use for automatic fee estimation."""

    gas_adjustment: Union[str, float, int, Dec]
    """Gas adjustment factor for automatic fee estimation."""

    last_request_height: Optional[int]  # type: ignore
    """Height of response of last-made made LCD request."""

    auth: AuthAPI
    """:class:`AuthAPI<terra_sdk.client.lcd.api.auth.AuthAPI>`."""

    bank: BankAPI
    """:class:`BankAPI<terra_sdk.client.lcd.api.bank.BankAPI>`."""

    distribution: DistributionAPI
    """:class:`DistributionAPI<terra_sdk.client.lcd.api.distribution.DistributionAPI>`."""

    gov: GovAPI
    """:class:`GovAPI<terra_sdk.client.lcd.api.gov.GovAPI>`."""

    market: MarketAPI
    """:class:`MarketAPI<terra_sdk.client.lcd.api.market.MarketAPI>`."""

    mint: MintAPI
    """:class:`MintAPI<terra_sdk.client.lcd.api.mint.MintAPI>`."""

    msgauth: MsgAuthAPI
    """:class:`MsgAuthAPI<terra_sdk.client.lcd.api.msgauth.MsgAuthAPI>`."""

    oracle: OracleAPI
    """:class:`OracleAPI<terra_sdk.client.lcd.api.oracle.OracleAPI>`."""

    slashing: SlashingAPI
    """:class:`SlashingAPI<terra_sdk.client.lcd.api.slashing.SlashingAPI>`."""

    staking: StakingAPI
    """:class:`StakingAPI<terra_sdk.client.lcd.api.staking.StakingAPI>`."""

    supply: SupplyAPI
    """:class:`SupplyAPI<terra_sdk.client.lcd.api.supply.SupplyAPI>`."""

    tendermint: TendermintAPI
    """:class:`TendermintAPI<terra_sdk.client.lcd.api.tendermint.TendermintAPI>`."""

    treasury: TreasuryAPI
    """:class:`TreasuryAPI<terra_sdk.client.lcd.api.treasury.TreasuryAPI>`."""

    wasm: WasmAPI
    """:class:`WasmAPI<terra_sdk.client.lcd.api.wasm.WasmAPI>`."""

    tx: TxAPI
    """:class:`TxAPI<terra_sdk.client.lcd.api.tx.TxAPI>`."""

    def __init__(
        self,
        url: str,
        chain_id: str = None,
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
    ):
        super().__init__(
            url,
            chain_id,
            gas_prices,
            gas_adjustment,
            _create_session=False,
            loop=nest_asyncio.apply(get_event_loop()),
        )

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
        """Creates a :class:`Wallet` object from a key for easy transaction creating and
        signing.

        Args:
            key (Key): key implementation
        """
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
