"""Tools for building WebSocket-based listeners."""
import asyncio
import base64
from typing import Any, Callable, List

from terra_sdk.core import TxInfo
from terra_sdk.core.event import Event
from terra_sdk.error import RpcError
from terra_sdk.query.event import EventsQuery
from terra_sdk.util import hash_amino
from terra_sdk.util.serdes import terra_sdkBox

__all__ = [
    "Ignore",
    "StopListening",
    "Unsubscribe",
    "Resubscribe",
    "TendermintEventListener",
    "TxListener",
    "BlockListener",
    "run_listeners",
    "Q",
]


class Ignore(Exception):
    """Raise to ignore the error."""


class StopListening(Exception):
    """Raise to stop listening."""


class Unsubscribe(Exception):
    """Raise to unsubscribe."""


class Resubscribe(Exception):
    """Raise to resubscribe."""


class TendermintEventListener(object):

    event = ""
    query = {}

    def __init__(
        self, terra, *, func: Callable[[TxInfo], Any] = None, query: dict = None
    ):
        self.terra = terra
        self.terra = terra
        self.func = func
        if query is not None:
            self.query = query  # otherwise, it is left as default ({})
        self.ws = None

    def on_message(self, msg):
        """Override this if you want access to the direct JSON-RPC parsed message. For
        implementing custom listeners."""
        pass

    def on_error(self, err: RpcError):
        """Implement `on_error`, which will be provided the RpcError, if encountered.
        Note that any other errors will not make it here, and should be handled in `on_tx`.

        With regard to execution, you can do one of four things:

        1) ignore the error

        >>> self.ignore()

        2) stop listening (stop execution)

        >>> self.stop_listening()

        3) unsubscribe

        >>> self.unsubscribe()

        4) resubscribe

        >>> self.resubscribe()

        If you do nothing, the error will be raised outside listening execution context.
        """
        pass

    async def _send_subscription_msg(self, tm_event, query, unsubscribe=False):
        # TODO: improve query ... can have stupid injection mistakes
        if not query:  # if query is not truthy; i.e. {}, '', None, ...
            query = ""
        else:
            if isinstance(query, dict):
                query = " AND ".join(f"{i[0]} = '{i[1]}'" for i in query.items())
            elif hasattr(query, "to_tmquery"):
                query = query.to_tmquery()
            else:  # use the string
                query = str(query)
            query = " AND " + query
        tm_query = f"tm.event = '{tm_event}'"
        sub_type = "subscribe" if not unsubscribe else "unsubscribe"
        resp = await self.terra.ws.request(
            self.ws, sub_type, params={"query": f"{tm_query}{query}"}
        )
        return self.terra.ws.handle_response(resp)

    async def _subscribe(self):
        """Performs the actual subscribing."""
        await self._send_subscription_msg(self.event, self.query)

    async def _unsubscribe(self):
        """Performs the actual unsubscribing."""
        await self._send_subscription_msg(self.event, self.query, unsubscribe=True)

    # error handling methods (these must be called inside `on_error`).

    def stop_listening(self):
        """Used inside `on_error`, tells the listener to stop listening."""
        raise StopListening

    def ignore(self):
        """Used inside `on_error`, tells the listener to ignore the error."""
        raise Ignore

    def resubscribe(self):
        """Used inside `on_error`, tells the listener to re-subscribe."""
        raise Resubscribe

    def unsubscribe(self):
        """Used inside `on_error`, tells the listener to unsubscribe."""
        raise Unsubscribe

    def __await__(self):
        async def listener():
            async with self.terra.ws.connect() as ws:
                self.ws = ws
                await self._subscribe()
                while True:
                    try:  # for stop listening
                        try:
                            async for resp in ws:
                                resp = self.terra.ws.handle_response(resp)
                                result = resp["result"]
                                self.on_message(result)
                        except RpcError as err:
                            try:
                                self.on_error(err)
                            except Ignore:
                                continue
                            except Unsubscribe:
                                await self._unsubscribe()
                                continue
                            except Resubscribe:
                                await self._unsubscribe()
                                await self._subscribe()
                                continue
                            raise err
                    except StopListening:
                        return

        return listener()


class TxListener(TendermintEventListener):

    event = "Tx"
    query = {}

    def _process_tx_msg(self, message):
        """Currently, the default behavior is to re-lookup the tranasaction via the LCD
        connection, because the result is amino-encoded. Follow this example to build
        your own version by overriding the default behavior in _process_tx_msg."""

        txresult = message["data"]["value"]["TxResult"]
        return self.terra.tx_info(hash_amino(txresult["tx"]))

    def on_message(self, message):
        tx = self._process_tx_msg(message)
        return self.on_tx(tx)

    def on_tx(self, tx: TxInfo):
        """Implement `on_tx`, which will be provided the transaction information received
        through the subscription.
        """
        if self.func:
            self.func(self, tx)


class BlockListener(TendermintEventListener):

    event = "NewBlock"
    query = {}

    @staticmethod
    def _decode_kvs_b64(atts: List[dict]):
        """Decodes base64 key-value pairs for events."""
        return [
            {
                "key": base64.b64decode(att["key"]).decode(),
                "value": base64.b64decode(att["value"]).decode(),
            }
            for att in atts
        ]

    def _process_block_msg(self, message) -> terra_sdkBox:
        """Will process the response from a NewBlock subscription and turn it into a
        block's context."""
        data = message["data"]["value"]
        height = data["block"]["header"]["height"]
        block = self.terra.blocks.at(height)
        begin_block_events = [
            {"type": e["type"], "attributes": self._decode_kvs_b64(e["attributes"])}
            for e in data["result_begin_block"].get("events", [])
        ]
        end_block_events = [
            {"type": e["type"], "attributes": self._decode_kvs_b64(e["attributes"])}
            for e in data["result_end_block"].get("events", [])
        ]
        return terra_sdkBox(
            {
                "block": block,
                "events": {
                    "begin_block": EventsQuery(
                        Event.deserialize(e) for e in begin_block_events
                    ),
                    "end_block": EventsQuery(
                        Event.deserialize(e) for e in end_block_events
                    ),
                },
            }
        )

    def on_message(self, message):
        block = self._process_block_msg(message)
        return self.on_block(block)

    def on_block(self, block_ctx: terra_sdkBox):
        """Implement `on_block`, which will be provided the block information received
        through the subscription.
        """
        if self.func:
            self.func(self, block_ctx)


def run_listeners(*listeners):
    """Runs all listeners until they all stop."""
    asyncio.get_event_loop().run_until_complete(asyncio.gather(*listeners))


# NOTE: The following is experimental.


class QueryBuilder:
    def __init__(self, path):
        self.path = path

    def eq(self, arg):
        return QueryNode("=", self.path, arg)

    def ne(self, arg):
        raise NotImplementedError(
            'operation can be "=", "<", "<=", ">", ">=", "CONTAINS" AND "EXISTS"'
        )

    def lt(self, arg):
        return QueryNode("<", self.path, arg)

    def le(self, arg):
        return QueryNode("<=", self.path, arg)

    def gt(self, arg):
        return QueryNode(">", self.path, arg)

    def ge(self, arg):
        return QueryNode(">=", self.path, arg)

    def __contains__(self, arg):
        return QueryNode("CONTAINS", self.path, arg)

    def contains(self, arg):
        return self.__contains__(arg)

    @property
    def exists(self):
        return ExistsNode(self.path)


class QueryNode:
    def __init__(self, op, path, arg):
        self.op = op
        self.path = path
        self.arg = arg

    def __and__(self, other):
        return AndNode(self, other)

    def to_tmquery(self):
        return f"{self.path} {self.op} {self.arg!r}"


class AndNode(QueryNode):
    def __init__(self, t1: QueryNode, t2: QueryNode):
        self.t1 = t1
        self.t2 = t2

    def to_tmquery(self):
        return f"{self.t1.to_tmquery()} AND {self.t2.to_tmquery()}"


class ExistsNode(QueryNode):
    def __init__(self, path):
        self.path = path

    def to_tmquery(self):
        return f"{self.path} EXISTS"


# Usage: Q("message.action").exists & Q("message.action").eq("3")
Q = QueryBuilder
