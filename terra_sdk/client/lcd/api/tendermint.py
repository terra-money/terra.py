from typing import Optional

from ._base import BaseAPI


class AsyncTendermintAPI(BaseAPI):
    async def node_info(self) -> dict:
        return await self._c._get("/node_info", raw=True)

    async def syncing(self) -> bool:
        return (await self._c._get("/syncing", raw=True))["syncing"]

    async def validator_set(self, height: Optional[int] = None) -> dict:
        x = "latest" if height is None else height
        return await self._c._get(f"/validatorsets/{x}")

    async def block_info(self, height: Optional[int] = None) -> dict:
        x = "latest" if height is None else height
        return await self._c._get(f"/blocks/{x}", raw=True)


class TendermintAPI(BaseAPI):
    def node_info(self) -> dict:
        """Fetches the curent connected node's information.

        Returns:
            dict: node information
        """
        return self._c._get("/node_info", raw=True)

    def syncing(self) -> bool:
        """Fetches whether the curent connect node is syncing with the network.

        Returns:
            bool: syncing status
        """
        return (self._c._get("/syncing", raw=True))["syncing"]

    def validator_set(self, height: Optional[int] = None) -> dict:
        """Fetches the validator set for a height. If no height is given, defaults to latest.

        Args:
            height (Optional[int], optional): block height. Defaults to None.

        Returns:
            dict: validator set
        """
        x = "latest" if height is None else height
        return self._c._get(f"/validatorsets/{x}")

    def block_info(self, height: Optional[int] = None) -> dict:
        """Fetches the block information for a given height. If no height is given, defaults to latest block.

        Args:
            height (Optional[int], optional): block height. Defaults to None.

        Returns:
            dict: block info
        """
        x = "latest" if height is None else height
        return self._c._get(f"/blocks/{x}", raw=True)
