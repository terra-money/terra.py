from functools import reduce
from math import ceil
from typing import Any, Dict, Union

from terra_sdk.core import Coin

from .api._base import BaseAsyncAPI, sync_bind


def index_by_pub_key(m: Dict[str, Any], o: Any):
    m[o["pub_key"]["key"]] = o
    return m


class AsyncLCDUtils(BaseAsyncAPI):
    async def validators_with_voting_power(self) -> Dict[str, dict]:
        """Gets current validators and merges their voting power from the validator set query.

        Returns:
            Dict[str, dict]: validators with voting power
        """
        validator_set_response = await BaseAsyncAPI._try_await(
            self._c.tendermint.validator_set()
        )
        next_key = ""
        while True:
            from terra_sdk.client.lcd import PaginationOptions

            validators, pag = await BaseAsyncAPI._try_await(
                self._c.staking.validators(PaginationOptions(key=next_key))
            )
            validator_set: Dict[str, Any] = reduce(
                index_by_pub_key, validator_set_response["validators"], {}
            )
            if pag is None or pag["next_key"] is None:
                break
            next_key = pag["next_key"]
        res = {}
        for v in validators:
            delegate_info = validator_set.get(v.consensus_pubkey["key"])
            if delegate_info is None:
                continue
            res[v.operator_address] = {
                "validator_info": v,
                "voting_power": int(delegate_info["voting_power"]),
                "proposer_priority": int(delegate_info["proposer_priority"]),
            }
        return res


class LCDUtils(AsyncLCDUtils):
    @sync_bind(AsyncLCDUtils.validators_with_voting_power)
    async def validators_with_voting_power(self) -> Dict[str, dict]:
        pass
