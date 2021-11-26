Common examples
==========
## Configuring LCDClient

```ts
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
```

.. automodule:: terra_sdk.exceptions
    :members:
