from typing import Dict, Optional, Union

import terra_sdk
from terra_sdk.client.lcd.api import project
from terra_sdk.client.lcd.api.modules import (
    AuthApi,
    BankApi,
    DistributionApi,
    GovApi,
    MarketApi,
    OracleApi,
    SlashingApi,
    StakingApi,
    SupplyApi,
    TreasuryApi
)
from terra_sdk.client.lcd.api.tendermint import TendermintApi
from terra_sdk.client.lcd.api.tx import TxApi
from terra_sdk.client.lcd.lcdclient import LcdClient
from terra_sdk.client.object_query import (
    AccountQuery,
    DenomQuery,
    ProposalQuery,
    ValidatorQuery,
    Wallet
)
from terra_sdk.client.websocket import WebSocketClient
from terra_sdk.core import AccAddress, Coins, ValAddress
from terra_sdk.error import DenomNotFound
from terra_sdk.listener import BlockListener, TxListener
from terra_sdk.util.serdes import terra_sdkBox
from terra_sdk.util.validation import validate_acc_address, validate_val_address


class Terra(object):
    def __init__(
        self,
        chain_id: str,
        lcd_url: str,
        ws_url: str = None,
        gas_prices: Coins = None,
        gas_adjustment: Union[float, str] = "1.4",  # sensible defaults
    ):
        gas_prices = gas_prices or Coins(uluna="0.015")  # sensible defaults

        self.gas_prices = gas_prices
        self.gas_adjustment = gas_adjustment

        # LCD APIs
        self.lcd = LcdClient(self, lcd_url)

        # LCD module APIs
        self._auth = AuthApi(self)
        self._bank = BankApi(self)
        self._supply = SupplyApi(self)
        self._distribution = DistributionApi(self)
        self._staking = StakingApi(self)
        self._slashing = SlashingApi(self)
        self._oracle = OracleApi(self)
        self._market = MarketApi(self)
        self._treasury = TreasuryApi(self)
        self._gov = GovApi(self)

        # LCD lower-level APIs
        self._tendermint = TendermintApi(self)
        self._tx = TxApi(self)

        # LCD query APIs
        self._blocks = terra_sdk.client.object_query.BlocksQuery(self)

        # if no chain_id, trust the node's chain_id
        if chain_id is None:
            # TODO: add warning if not same!
            self.chain_id = self.node_info()["node_info"]["network"]
        else:
            self.chain_id = chain_id

        # WebSocket APIs
        self.ws = WebSocketClient(self, ws_url)

    def __repr__(self):
        s = self
        return f"Terra('{s.chain_id}', '{s.lcd.url}')"

    def __str__(self):
        return f"{self.chain_id} via {self.lcd.url}"

    # Terra Core Module APIs provided through LCD:

    @property
    def auth(self):
        return self._auth

    @property
    def bank(self):
        return self._bank

    def supply(self, denom: Optional[str] = None):
        total_supply = self._supply.total()
        if denom is None:
            return total_supply
        if denom not in total_supply:
            raise DenomNotFound(
                f"denom '{denom}' was not found, avaialble denoms are: {total_supply.denoms}"
            )
        return project(total_supply, total_supply[denom])

    @property
    def distribution(self):
        return self._distribution

    @property
    def staking(self):
        return self._staking

    @property
    def slashing(self):
        return self._slashing

    @property
    def oracle(self):
        return self._oracle

    @property
    def market(self):
        return self._market

    @property
    def treasury(self):
        return self._treasury

    @property
    def gov(self):
        return self._gov

    @property
    def tx(self):
        return self._tx

    def is_connected(self) -> bool:
        """Checks that a connection can be made to the node specified, and has the same `chain_id`."""
        try:
            node_info = self.node_info()
            return self.chain_id == node_info["node_info"]["network"]
        except:  # not recommended, but if we run into any error, we are not connected.
            return False

    # lower-level APIs

    def is_syncing(self) -> bool:
        """Checks whether the node is currently syncing with the blockchain."""
        return self._tendermint.syncing()

    def node_info(self) -> Dict[str, dict]:
        """Get information about the node."""
        return self._tendermint.node_info()

    # Convenient Aliases for TX

    def tx_info(self, *args, **kwargs):
        return self._tx.tx_info(*args, **kwargs)

    def estimate_fee(self, *args, **kwargs):
        return self._tx.estimate_fee(*args, **kwargs)

    def broadcast(self, *args, **kwargs):
        return self._tx.broadcast(*args, **kwargs)

    # Object query based APIs

    def account(self, arg: AccAddress) -> AccountQuery:
        arg = validate_acc_address(arg)
        return AccountQuery(self, arg)

    def validator(self, arg: ValAddress) -> ValidatorQuery:
        arg = validate_val_address(arg)
        return ValidatorQuery(self, arg)

    def denom(self, arg: str) -> DenomQuery:
        return DenomQuery(self, arg)

    def wallet(self, arg: terra_sdk.key.Key) -> Wallet:
        return Wallet(self, arg)

    def proposal(self, proposal_id: int) -> ProposalQuery:
        return ProposalQuery(self, proposal_id)

    ##

    @property
    def blocks(self):
        """Blocks querying API."""
        return self._blocks

    def block(self, height=None):
        """Get the block at a specific height."""
        return self._blocks.at(height)

    def delegates(self, height=None):
        all_validators = self.staking.validators()
        vset = self._tendermint.validator_set(height=height)
        # join validators using pubkey
        by_pubkey = {x["pub_key"]: x for x in vset}
        return terra_sdkBox(
            {
                v.operator_address: {"info": v, **by_pubkey[v.consensus_pubkey]}
                for v in all_validators
                if v.consensus_pubkey in by_pubkey
            }
        )

    ## WebSockets

    def tx_listener(self, query: dict = None):
        def decorator(f):
            return TxListener(self, func=f, query=query)

        return decorator

    def block_listener(self, query: dict = None):
        def decorator(f):
            return BlockListener(self, func=f, query=query)

        return decorator
