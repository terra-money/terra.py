import base64
import copy
from typing import List, Optional

import attr
from multidict import CIMultiDict

from terra_sdk.core import AccAddress, Coins, Dec, Numeric, PublicKey
from terra_sdk.core.broadcast import (
    AsyncTxBroadcastResult,
    BlockTxBroadcastResult,
    SyncTxBroadcastResult,
)
from terra_sdk.core.fee import Fee
from terra_sdk.core.msg import Msg
from terra_sdk.core.tx import AuthInfo, SignerData, SignMode, Tx, TxBody, TxInfo
from terra_sdk.util.hash import hash_amino
from terra_sdk.util.json import JSONSerializable

from ..params import APIParams
from ._base import BaseAsyncAPI, sync_bind

__all__ = [
    "AsyncTxAPI",
    "TxAPI",
    "BroadcastOptions",
    "CreateTxOptions",
    "SignerOptions",
]


@attr.s
class SignerOptions:
    """SignerOptions specifies infomations about signers
    Args:
        address (AccAddress): address of the signer
        sequence (int, optional): nonce of the messages from the signer
        public_key (PublicKey, optional): signer's PublicKey
    """

    address: AccAddress = attr.ib()
    sequence: Optional[int] = attr.ib(default=None)
    public_key: Optional[PublicKey] = attr.ib(default=None)


@attr.s
class CreateTxOptions:
    """

    Args:
        msgs (List[Msg]): list of messages to include
        fee (Optional[Fee], optional): transaction fee. If ``None``, will be estimated.
            See more on `fee estimation`_.
        memo (str, optional): optional short string to include with transaction.
        gas (str, optional): gas limit to set per-transaction; set to "auto" to calculate sufficient gas automatically
        gas_prices (Coins.Input, optional): gas prices for fee estimation.
        gas_adjustment (Numeric.Input, optional): gas adjustment for fee estimation.
        fee_denoms (List[str], optional): list of denoms to use for fee after estimation.
        account_number (int, optional): account number (overrides blockchain query if
            provided)
        sequence (int, optional): sequence (overrides blockchain qu ery if provided)
        timeout_height (int, optional):  specifies a block timeout height to prevent the tx from being committed past a certain height.
        sign_mode: (SignMode, optional): SignMode.SIGN_MODE_DIRECT by default. multisig needs SignMode.SIGN_MODE_LEGACY_AMINO_JSON.
    """

    msgs: List[Msg] = attr.ib()
    fee: Optional[Fee] = attr.ib(default=None)
    memo: Optional[str] = attr.ib(default=None)
    gas: Optional[str] = attr.ib(default=None)
    gas_prices: Optional[Coins.Input] = attr.ib(default=None)
    gas_adjustment: Optional[Numeric.Output] = attr.ib(
        default=0, converter=Numeric.parse
    )
    fee_denoms: Optional[List[str]] = attr.ib(default=None)
    account_number: Optional[int] = attr.ib(default=None)
    sequence: Optional[int] = attr.ib(default=None)
    timeout_height: Optional[int] = attr.ib(default=None)
    sign_mode: Optional[SignMode] = attr.ib(default=None)


@attr.s
class BroadcastOptions:
    sequences: Optional[List[int]] = attr.ib()
    fee_granter: Optional[AccAddress] = attr.ib(default=None)


""" deprecated
@attr.s
class TxSearchOption:
    key: str = attr.ib()
    value: Union[str, int] = attr.ib()
"""


@attr.s
class GasInfo:
    gas_wanted: int = attr.ib(converter=int)
    gas_used: int = attr.ib(converter=int)


@attr.s
class EventAttribute:
    key: str = attr.ib()
    value: str = attr.ib()


@attr.s
class Event:
    type: str = attr.ib()
    attributes: List[EventAttribute] = attr.ib(converter=list)


@attr.s
class SimulateResult:
    data: str = attr.ib()
    log: str = attr.ib()
    events: List[Event] = attr.ib(converter=list)


@attr.s
class SimulateResponse(JSONSerializable):
    gas_info: GasInfo = attr.ib()
    result: SimulateResult = attr.ib()

    @classmethod
    def from_data(cls, data: dict):
        return cls(gas_info=data["gas_info"], result=data["result"])


class AsyncTxAPI(BaseAsyncAPI):
    async def tx_info(self, tx_hash: str) -> TxInfo:
        """Fetches information for an included transaction given a tx hash.

        Args:
            tx_hash (str): hash of transaction to lookup

        Returns:
            TxInfo: transaction info
        """
        res = await self._c._get(f"/cosmos/tx/v1beta1/txs/{tx_hash}")
        return TxInfo.from_data(res["tx_response"])

    async def create(
        self, signers: List[SignerOptions], options: CreateTxOptions
    ) -> Tx:
        """Create a new unsigned transaction, with helpful utilities such as lookup of
        chain ID, account number, sequence and fee estimation.

        Args:
            signers (List[SignerOptions]): options about signers
            options (CreateTxOptions): options about creating a tx

        Returns:
            Tx: unsigned tx
        """

        opt = copy.deepcopy(options)

        signer_data: List[SignerData] = []
        for signer in signers:
            seq = signer.sequence
            pubkey = signer.public_key

            if seq is None or pubkey is None:
                acc = await BaseAsyncAPI._try_await(
                    self._c.auth.account_info(signer.address)
                )
                if seq is None:
                    seq = acc.get_sequence()
                if pubkey is None:
                    pubkey = acc.get_public_key()
            signer_data.append(SignerData(seq, pubkey))

        # create the fake fee
        if opt.fee is None:
            opt.fee = await BaseAsyncAPI._try_await(self.estimate_fee(signer_data, opt))

        return Tx(
            TxBody(opt.msgs, opt.memo or "", opt.timeout_height or 0),
            AuthInfo([], opt.fee),
            [],
        )

    async def estimate_fee(
        self, signers: List[SignerOptions], options: CreateTxOptions
    ) -> Fee:
        """Estimates the proper fee to apply by simulating it within the node.

        Args:
            signers ([SignerOptions]): signers
            options (CreateTxOptions): transaction info to estimate fee

        Returns:
            Fee: estimated fee
        """

        gas_prices = options.gas_prices or self._c.gas_prices
        gas_adjustment = options.gas_adjustment or self._c.gas_adjustment

        gas_prices_coins = None
        if gas_prices:
            gas_prices_coins = Coins(gas_prices)
            if options.fee_denoms:
                _fee_denoms = options.fee_denoms if options.fee_denoms else ["uluna"]
                gas_prices_coins = gas_prices_coins.filter(
                    lambda c: c.denom in _fee_denoms
                )
        tx_body = TxBody(messages=options.msgs, memo=options.memo or "")
        emptyCoins = Coins()
        emptyFee = Fee(0, emptyCoins)
        auth_info = AuthInfo([], emptyFee)

        tx = Tx(tx_body, auth_info, [])
        tx.append_empty_signatures(signers)

        gas = options.gas
        if gas is None or gas == "auto" or int(gas) == 0:
            opt = copy.deepcopy(options)
            opt.gas_adjustment = gas_adjustment
            gas = str(await super()._try_await(self.estimate_gas(tx, opt)))

        fee_amount = (
            gas_prices_coins.mul(gas).to_int_ceil_coins()
            if gas_prices_coins
            else Coins.from_str("0uluna")
        )

        return Fee(Numeric.parse(gas), fee_amount, "", "")

    async def estimate_gas(self, tx: Tx, options: Optional[CreateTxOptions]) -> int:
        gas_adjustment = options.gas_adjustment if options else self._c.gas_adjustment

        res = await self._c._post(
            "/cosmos/tx/v1beta1/simulate",
            {"tx_bytes": await super()._try_await(self.encode(tx))},
        )
        simulated = SimulateResponse.from_data(res)

        return int(Dec(gas_adjustment).mul(simulated.gas_info["gas_used"]))

    async def encode(self, tx: Tx) -> str:
        """Encode a Tx to base64 encoded proto string"""
        return base64.b64encode(bytes(tx.to_proto())).decode()

    async def decode(self, tx: str) -> Tx:
        """Decode base64 encoded proto string to a Tx"""
        return Tx.from_bytes(base64.b64decode(tx))

    async def hash(self, tx: Tx) -> str:
        """Compute hash for a transaction.

        Args:
            tx (Tx): transaction to hash

        Returns:
            str: transaction hash
        """
        amino = await super()._try_await(self.encode(tx))
        return hash_amino(amino)

    async def _broadcast(
        self, tx: Tx, mode: str, options: BroadcastOptions = None
    ) -> dict:
        data = {"tx_bytes": await super()._try_await(self.encode(tx)), "mode": mode}
        return await self._c._post("/cosmos/tx/v1beta1/txs", data)  # , raw=True)

    async def broadcast_sync(
        self, tx: Tx, options: BroadcastOptions = None
    ) -> SyncTxBroadcastResult:
        """Broadcasts a transaction using the ``sync`` broadcast mode.

        Args:
            tx (Tx): transaction to broadcast
            options (BroadcastOptions): broacast options, optional

        Returns:
            SyncTxBroadcastResult: result
        """
        res = await self._broadcast(tx, "BROADCAST_MODE_SYNC", options)
        res = res.get("tx_response")
        return SyncTxBroadcastResult(
            txhash=res.get("txhash"),
            raw_log=res.get("raw_log"),
            code=res.get("code"),
            codespace=res.get("codespace"),
        )

    async def broadcast_async(
        self, tx: Tx, options: BroadcastOptions = None
    ) -> AsyncTxBroadcastResult:
        """Broadcasts a transaction using the ``async`` broadcast mode.

        Args:
            tx (Tx): transaction to broadcast
            options (BroadcastOptions): broacast options, optional

        Returns:
            AsyncTxBroadcastResult: result
        """
        res = await self._broadcast(tx, "BROADCAST_MODE_ASYNC", options)
        res = res.get("tx_response")
        return AsyncTxBroadcastResult(
            txhash=res.get("txhash"),
        )

    async def broadcast(
        self, tx: Tx, options: BroadcastOptions = None
    ) -> BlockTxBroadcastResult:
        """Broadcasts a transaction using the ``block`` broadcast mode.

        Args:
            tx (Tx): transaction to broadcast
            options (BroadcastOptions): broacast options, optional

        Returns:
            BlockTxBroadcastResult: result
        """
        res = await self._broadcast(tx, "BROADCAST_MODE_BLOCK", options)
        res = res["tx_response"]
        return BlockTxBroadcastResult(
            height=res.get("height") or 0,
            txhash=res.get("txhash"),
            raw_log=res.get("raw_log"),
            gas_wanted=res.get("gas_wanted") or 0,
            gas_used=res.get("gas_used") or 0,
            logs=res.get("logs"),
            code=res.get("code"),
            codespace=res.get("codespace"),
        )

    async def search(
        self, events: List[list], params: Optional[APIParams] = None
    ) -> dict:
        """Searches for transactions given criteria.

        Args:
            events (dict): dictionary containing options
            params (APIParams): optional parameters

        Returns:
            dict: transaction search results
        """

        actual_params = CIMultiDict()

        for event in events:
            if event[0] == "tx.height":
                actual_params.add("events", f"{event[0]}={event[1]}")
            else:
                actual_params.add("events", f"{event[0]}='{event[1]}'")
        if params:
            for p in params:
                actual_params.add(p, params[p])

        res = await self._c._get("/cosmos/tx/v1beta1/txs", actual_params)
        return {
            "txs": [TxInfo.from_data(tx) for tx in res.get("tx_responses")],
            "pagination": res.get("pagination"),
        }

    async def tx_infos_by_height(self, height: Optional[int] = None) -> List[TxInfo]:
        """Fetches information for an included transaction given block height or latest

        Args:
            height (int, optional): height to lookup. latest if height is None.

        Returns:
            List[TxInfo]: transaction info
        """
        if height is None:
            x = "latest"
        else:
            x = height

        res = await self._c._get(f"/cosmos/base/tendermint/v1beta1/blocks/{x}")

        txs = res.get("block").get("data").get("txs")
        hashes = [hash_amino(tx) for tx in txs]
        return [
            await BaseAsyncAPI._try_await(self.tx_info(tx_hash)) for tx_hash in hashes
        ]


class TxAPI(AsyncTxAPI):
    @sync_bind(AsyncTxAPI.tx_info)
    def tx_info(self, tx_hash: str) -> TxInfo:
        pass

    tx_info.__doc__ = AsyncTxAPI.tx_info.__doc__

    @sync_bind(AsyncTxAPI.create)
    def create(self, signers: List[SignerOptions], options: CreateTxOptions) -> Tx:
        pass

    create.__doc__ = AsyncTxAPI.create.__doc__

    @sync_bind(AsyncTxAPI.estimate_fee)
    def estimate_fee(
        self, signers: List[SignerOptions], options: CreateTxOptions
    ) -> Fee:
        pass

    estimate_fee.__doc__ = AsyncTxAPI.estimate_fee.__doc__

    @sync_bind(AsyncTxAPI.estimate_gas)
    def estimate_gas(
        self, tx: Tx, options: Optional[CreateTxOptions]
    ) -> SimulateResponse:
        pass

    estimate_gas.__doc__ = AsyncTxAPI.estimate_gas.__doc__

    @sync_bind(AsyncTxAPI.encode)
    def encode(self, tx: Tx) -> str:
        pass

    encode.__doc__ = AsyncTxAPI.encode.__doc__

    @sync_bind(AsyncTxAPI.decode)
    def decode(self, tx: str) -> Tx:
        pass

    decode.__doc__ = AsyncTxAPI.decode.__doc__

    @sync_bind(AsyncTxAPI.hash)
    def hash(self, tx: Tx) -> str:
        pass

    hash.__doc__ = AsyncTxAPI.hash.__doc__

    @sync_bind(AsyncTxAPI.broadcast_sync)
    def broadcast_sync(
        self, tx: Tx, options: BroadcastOptions = None
    ) -> SyncTxBroadcastResult:
        pass

    broadcast_sync.__doc__ = AsyncTxAPI.broadcast_sync.__doc__

    @sync_bind(AsyncTxAPI.broadcast_async)
    def broadcast_async(
        self, tx: Tx, options: BroadcastOptions = None
    ) -> AsyncTxBroadcastResult:
        pass

    broadcast_async.__doc__ = AsyncTxAPI.broadcast_async.__doc__

    @sync_bind(AsyncTxAPI.broadcast)
    def broadcast(
        self, tx: Tx, options: BroadcastOptions = None
    ) -> BlockTxBroadcastResult:
        pass

    broadcast.__doc__ = AsyncTxAPI.broadcast.__doc__

    @sync_bind(AsyncTxAPI.search)
    def search(self, events: List[list], params: Optional[APIParams] = None) -> dict:
        pass

    search.__doc__ = AsyncTxAPI.search.__doc__

    @sync_bind(AsyncTxAPI.tx_infos_by_height)
    def tx_infos_by_height(self, height: Optional[int] = None) -> List[TxInfo]:
        pass

    tx_infos_by_height.__doc__ = AsyncTxAPI.tx_infos_by_height.__doc__
