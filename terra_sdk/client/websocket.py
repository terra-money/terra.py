import asyncio
import json
from urllib.parse import urljoin

import websockets

from terra_sdk.error import RpcError, get_rpc_error
from terra_sdk.util import hash_amino
from terra_sdk.util.serdes import terra_sdkBox


class WebSocketClient(object):
    def __init__(self, terra, ws_url: str = "", ssl_context=None):
        self.terra = terra
        self.url = ws_url
        self.ssl_context = ssl_context

    def _create_url(self, path):
        return urljoin(self.url, path)

    def connect(self, path="websocket"):
        url = self._create_url(path)
        if self.ssl_context is not None or url.startswith("wss"):
            return websockets.connect(
                self._create_url(path), ssl=self.ssl_context or True
            )
        else:
            return websockets.connect(self._create_url(path))

    @staticmethod
    async def request(ws, method, params={}, id="0"):
        await ws.send(
            json.dumps(
                {"jsonrpc": "2.0", "method": method, "id": id, "params": params,}
            )
        )
        return await ws.recv()

    @staticmethod
    def handle_response(resp: str) -> dict:
        resp = json.loads(resp)
        if "error" in resp:
            raise get_rpc_error(resp["error"]["code"], resp["error"]["data"])
        return resp
