import json
from typing import Any

from ._base import BaseAPI


class AsyncWasmAPI(BaseAPI):
    async def code_info(self, code_id: int) -> dict:
        return await self._c._get(f"/wasm/codes/{code_id}")

    async def contract_info(self, contract_address: str) -> dict:
        res = await self._c._get(f"/wasm/contracts/{contract_address}")
        return res

    async def contract_query(self, contract_address: str, query: dict) -> Any:
        params = {"query_msg": json.dumps(query)}
        return await self._c._get(f"/wasm/contracts/{contract_address}/store", params)

    async def parameters(self) -> dict:
        return await self._c._get("/wasm/parameters")


class WasmAPI(BaseAPI):
    def code_info(self, code_id: int) -> dict:
        """Fetches information about an uploaded code.

        Args:
            code_id (int): code ID

        Returns:
            dict: code information
        """
        return self._c._get(f"/wasm/codes/{code_id}")

    def contract_info(self, contract_address: str) -> dict:
        """Fetches information about an instantiated contract.

        Args:
            contract_address (str): contract address

        Returns:
            dict: contract information
        """
        res = self._c._get(f"/wasm/contracts/{contract_address}")
        return res

    def contract_query(self, contract_address: str, query_msg: dict) -> Any:
        """Runs a QueryMsg on a contract.

        Args:
            contract_address (str): contract address
            query_msg (dict): QueryMsg to run

        Returns:
            Any: results of query
        """
        params = {"query_msg": json.dumps(query_msg)}
        return self._c._get(f"/wasm/contracts/{contract_address}/store", params)

    def parameters(self) -> dict:
        """Fetches the Wasm module parameters.

        Returns:
            dict: Wasm module parameters
        """
        return self._c._get("/wasm/parameters")
