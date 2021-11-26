Common examples
====================

Configuring LCDClient
============================
The following code example shows how to initialize the LCDClient. The rest of the examples assume you initialized it by using this example or similar code.

class AsyncLCDClient:
    def __init__(
        self,
        url: str,
        chain_id: Optional[str] = None,
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
        loop: Optional[AbstractEventLoop] = None,
        _create_session: bool = True,  # don't create a session (used for sync LCDClient)
    ):

Creating a wallet for easy transaction creating and signing
==========

The following code example shows how to create a wallet to store transactions. 

    def wallet(self, key: Key) -> AsyncWallet:
        """Creates a :class:`AsyncWallet` object from a key.
        Args:
            key (Key): key implementation
        """
        return AsyncWallet(self, key)


Get transactions for synchronous client
==========
There is an object representing a connection to a node running the Terra LCD server. This function "get" session has to be manually created and torn down for each HTTP request in a synchronous client. 

    async def _get(
        self, endpoint: str, params: Optional[dict] = None, raw: bool = False
    ):
        async with self.session.get(
            urljoin(self.url, endpoint), params=params
        ) as response:
            try:
                result = await response.json(content_type=None)
            except JSONDecodeError:
                raise LCDResponseError(message=str(response.reason), response=response)
            if not 200 <= response.status < 299:
                raise LCDResponseError(message=result.get("error"), response=response)
        self.last_request_height = result.get("height")
        return result if raw else result["result"]



Post transactions for synchronous client
==========
here is an object representing a connection to a node running the Terra LCD server. The function "post" session has to be manually created and torn down for each HTTP request in a synchronous client. When th client is active, his/her transactions are posted and live for viewing. 

    async def _post(
        self, endpoint: str, data: Optional[dict] = None, raw: bool = False
    ):
        async with self.session.post(
            urljoin(self.url, endpoint), json=data and dict_to_data(data)
        ) as response:
            try:
                result = await response.json(content_type=None)
            except JSONDecodeError:
                raise LCDResponseError(message=str(response.reason), response=response)
            if not 200 <= response.status < 299:
                raise LCDResponseError(message=result.get("error"), response=response)
        self.last_request_height = result.get("height")
        return result if raw else result["result"]

.. automodule:: terra_sdk.exceptions
    :members:
