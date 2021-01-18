"""Low-level Tendermint Node API."""
from typing import List, Union

from terra_sdk.client.lcd.api import ApiResponse, BaseApi, project
from terra_sdk.util.serdes import terra_sdkBox

__all__ = ["TendermintApi"]


class TendermintApi(BaseApi):
    def node_info(self) -> Union[ApiResponse, terra_sdkBox]:
        """Get information for the node.
        Returns:
            Node information with the following schema.
        """
        res = self._api_get("/node_info", unwrap=False)
        return project(res, terra_sdkBox(res))

    def syncing(self) -> Union[ApiResponse, bool]:
        """Get whether the node is currently syncing with updates on the blockchain.

        Returns:
            If node is syncing.
        """
        res = self._api_get("/syncing", unwrap=False)
        return project(res, res["syncing"])

    def block(self, height=None) -> Union[ApiResponse, dict]:
        """Get the raw block data at a height on the blockchain.

        Args:
            height (int, optional): block height

        Returns:
            - The block at the provided height. If no height was specified, get the latest
            block at the time of calling.

        """
        if height:
            res = self._api_get(f"/blocks/{height}", unwrap=False)
        else:
            res = self._api_get("/blocks/latest", unwrap=False)
        return project(res, terra_sdkBox(res))

    def validator_set(self, height=None) -> Union[ApiResponse, dict]:
        """Retrieves the current set of validators in the actively validating set.

        ## Arguments
        - **height** `int` *optional*

            block height

        ## Returns
        List of `dict` with the following keys:

        - **address** `ValConsAddress`

            validator's consensus address

        - **pub_key** `ValConsPubKey`

            validator's consensus public key

        - **proposer_priority** `int`
        - **voting_power** `int`
        """
        if height:
            res = self._api_get(f"/validatorsets/{height}")
        else:
            res = self._api_get("/validatorsets/latest")
        vs = res["validators"]
        results = []
        for v in vs:
            results.append(
                terra_sdkBox(
                    {
                        "address": v["address"],
                        "pub_key": v["pub_key"],
                        "proposer_priority": int(v["proposer_priority"]),
                        "voting_power": int(v["voting_power"]),
                    }
                )
            )
        return project(res, results)
