import json
from typing import Any

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncWasmAPI", "WasmAPI"]


class AsyncWasmAPI(BaseAsyncAPI):
    async def code_info(self, code_id: int) -> dict:
        """Fetches information about an uploaded code.

        Args:
            code_id (int): code ID

        Returns:
            dict: code information
        """
        return await self._c._get(f"/wasm/codes/{code_id}")

    async def contract_info(self, contract_address: str) -> dict:
        """Fetches information about an instantiated contract.

        Args:
            contract_address (str): contract address

        Returns:
            dict: contract information
        """
        res = await self._c._get(f"/wasm/contracts/{contract_address}")
        return res

    async def contract_query(self, contract_address: str, query: dict) -> Any:
        """Runs a QueryMsg on a contract.

        Args:
            contract_address (str): contract address
            query_msg (dict): QueryMsg to run

        Returns:
            Any: results of query
        """
        params = {"query_msg": json.dumps(query)}
        return await self._c._get(f"/wasm/contracts/{contract_address}/store", params)

    async def parameters(self) -> dict:
        """Fetches the Wasm module parameters.

        Returns:
            dict: Wasm module parameters
        """
        return await self._c._get("/wasm/parameters")


class WasmAPI(AsyncWasmAPI):
    @sync_bind(AsyncWasmAPI.code_info)
    def code_info(self, code_id: int) -> dict:
        pass

    code_info.__doc__ = AsyncWasmAPI.code_info.__doc__

    @sync_bind(AsyncWasmAPI.contract_info)
    def contract_info(self, contract_address: str) -> dict:
        pass

    contract_info.__doc__ = AsyncWasmAPI.code_info.__doc__

    @sync_bind(AsyncWasmAPI.contract_query)
    def contract_query(self, contract_address: str, query_msg: dict) -> Any:
        pass

    contract_query.__doc__ = AsyncWasmAPI.contract_query.__doc__

    @sync_bind(AsyncWasmAPI.parameters)
    def parameters(self) -> dict:
        pass

    parameters.__doc__ = AsyncWasmAPI.parameters.__doc__
