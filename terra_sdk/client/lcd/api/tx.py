"""Low-level transaction API"""
import json
from typing import Union

from terra_sdk.client.lcd.api import ApiResponse, BaseApi, project
from terra_sdk.core import Coin, Coins, StdFee, StdSignMsg, StdTx, TxBroadcastResult, TxInfo
from terra_sdk.error import RpcError, TxError, get_codespace_error
from terra_sdk.util import hash_amino

# TODO: add tx transformer like blocks.transformer() to accomodate for custom messages
# ideal usage: terra.tx.transformer = my_transformer

__all__ = ["TxApi"]


class TxApi(BaseApi):
    """Low-level transactions API that interacts directly with the Tendermint logic of
    the node. Handles things that require on-chain connection such as hashing, amino-encoding,
    broadcasting, and transaction lookups.
    """

    def tx_info(self, txhash: Union[str]) -> Union[ApiResponse, TxInfo]:
        """Get the information for a transaction by its hash.

        :param txhash: transaction hash to lookup
        :type txhash: str

        Returns:
            Transaction info if found, otherwise `None`.
        """
        # TODO: add tx schema checking / error handling?
        res = self._api_get(f"/txs/{txhash}", unwrap=False)
        return project(res, TxInfo.deserialize(res))

    def _tx_info_threaded(self, txhashes):
        """Threaded version of tx_info, takes in a list of transaction hashes instead of
        just one transaction hash."""
        paths = [f"/txs/{txhash}" for txhash in txhashes]
        responses = self.lcd.get_threaded(paths)
        api_responses = [  # turn into API responses
            self._handle_response(resp, unwrap=False) for resp in responses
        ]
        return [project(res, TxInfo.deserialize(res)) for res in api_responses]

    def estimate_fee(
        self,
        tx: Union[StdSignMsg, StdTx],
        gas_prices: Coins = None,
        gas_adjustment: Union[float, str] = None,
    ) -> Union[ApiResponse, StdFee]:
        """Estimate a transaction's fee by simulating it in the node.

        Args:
            tx (Union[StdSignMsg, StdTx]): Transaction to calculate fee for.
            gas_prices (Coins, optional): Gas prices to use for estimation.
            gas_adjustment (Union[float, str], optional, default=1.0): Multiplicative
                factor to adjust for potential error.

        Returns:
            Estimated fee for the transaction.
        """
        if gas_prices is None:
            gas_prices = self.terra.gas_prices
        if gas_adjustment is None:
            gas_adjustment = self.terra.gas_adjustment
        if isinstance(tx, StdSignMsg):
            tx = tx.to_tx()
        tx.fee = StdFee(
            gas=0,  # simulation mode
            amount=Coins(
                Coin(d, 1) for d in gas_prices.denoms
            ),  # set 1 per denom we are including
        )
        data = {
            "tx": tx,
            "gas_adjustment": str(gas_adjustment),
            "gas_prices": gas_prices,
        }
        res = self._api_post("/txs/estimate_fee", data=data)
        gas = int(res["gas"])
        fees = Coins.deserialize(res["fees"])
        return project(res, StdFee(gas=gas, amount=fees))

    def encode(self, tx: StdTx) -> Union[ApiResponse, str]:
        """Generate the transaction's Amino enconding.

        Args:
            tx (StdTx): The transaction to encode.

        Returns:
            Base64-encoded string.
        """
        res = self._api_post("/txs/encode", data=tx, unwrap=False)
        return project(res, res["tx"])

    def hash(self, tx: StdTx) -> Union[ApiResponse, str]:
        """Gets the hash of a StdTx. This is in the Tx API due to the fact that terra_sdk
        must contact the server first, as Amino is not yet available on Python."""
        res = self.encode(tx)
        return project(res, hash_amino(res))

    def broadcast(
        self, tx: StdTx, mode: str = "block"
    ) -> Union[ApiResponse, TxBroadcastResult]:
        """Broadcast a signed transaction.

        :param tx: The signed transaction to broadcast.
        :param mode: One of "block", "sync", "async"
        """
        if mode not in ["block", "sync", "async"]:
            raise ValueError(
                f"mode '{mode}' is not legal; mode can only be 'block', 'sync', or 'async'."
            )
        data = {"tx": tx.to_data()["value"], "mode": mode}
        try:
            res = self._api_post("/txs", data=data, unwrap=False)
        except RpcError as e:
            raise TxError(e.message, tx)
        if "code" in res:  # status code 200, but TxError
            err = json.loads(res["raw_log"])
            # There are 2 types of Codespace errors that will be caught here:
            # 1) Message error : originating from a message
            # 2) Transaction : stuff like out of gas, insufficient fee, etc.
            #
            # If message error, `err` will be a list with the following structure:
            #
            # {'msg_index': 0, 'success': False, 'log': '{"codespace":"market","code":2,
            # "message":"No price registered with the oracle for asset: usdr"}', 'events':
            # [{'type': 'message', 'attributes': [{'key': 'action', 'value': 'swap'}]}]}
            #
            # Otherwise, `err` will be like (example).
            #
            # {"codespace":"market","code":2,
            # "message":"No price registered with the oracle for asset: usdr"}
            if isinstance(
                err, list
            ):  # encountered a msg-error; find the offending msg (there will only be 1)
                err = json.loads(err[-1]["log"])  # last one was the one responsible
            raise get_codespace_error(
                err["codespace"],
                err["code"],
                err["message"],
                was_from_tx=True,
                tx=tx,
                broadcast_result=TxBroadcastResult.from_data(res, tx),
            )
        retval = TxBroadcastResult.from_data(res, tx)
        return project(res, retval)
